/**
 * @author      : seid mohammad reza hodaee
 * @file        : main
 */

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define MAX_BUFFER_SIZE 1024

typedef char bit;

bit bit_parse(uint8_t v) { return v + '0'; }
uint8_t bit_value(bit v) { return v - '0'; }

void bit_arr_from_num(int n, uint8_t num, bit arr[])
{
    for (int i = 0; i < n; i++)
    {
        arr[n - i - 1] = bit_parse(num % 2);
        num /= 2;
    }
}
uint8_t bit_arr_to_num(int n, bit arr[])
{
    uint8_t ret = 0;
    for (int i = 0; i < n; i++)
        ret += bit_value(arr[n - i - 1]) << i;
    return ret;
}

void uint8_arr_invert_of_permutation(int n, uint8_t src[n], uint8_t dst[n])
{
    for (int i = 0; i < n; i++)
        dst[src[i] - 1] = i + 1;
}

void uint8_arr_print(int n, uint8_t src[n])
{
    printf("[");
    for (int i = 0; i < n - 1; i++)
        printf("%d,", src[i]);
    printf("%d]\n", src[n - 1]);
}

void bit_arr_print(int n, const bit arr[n])
{
    for (int i = 0; i < n; i++)
        putchar(arr[i]);
}

void bit_arr_permute_by_map(int nsrc, int ndst, const bit src[nsrc], bit dst[ndst], uint8_t map[ndst])
{
    for (int i = 0; i < ndst; i++)
        dst[i] = src[map[i] - 1];
}

void bit_arr_left_shift(int n, int r, const bit src[n], bit dst[n])
{
    for (int i = 0; i < n; i++)
        dst[i] = src[(i + r) % n];
}

void bit_arr_split_half(int n, const bit src[n], bit left[n / 2], bit right[n / 2])
{
    for (int i = 0; i < n / 2; i++)
    {
        left[i] = src[i];
        right[i] = src[i + n / 2];
    }
}

void bit_arr_combine(int n, const bit a[n / 2], const bit b[n / 2], bit dst[n])
{
    for (int i = 0; i < n / 2; i++)
    {
        dst[i] = a[i];
        dst[i + n / 2] = b[i];
    }
}

void bit_arr_xor(int n, const bit a[n], const bit b[n], bit dst[n])
{
    for (int i = 0; i < n; i++)
        dst[i] = bit_parse(bit_value(a[i]) ^ bit_value(b[i]));
}

void bit_arr_copy(int n, bit src[n], bit dst[n])
{
    for (int i = 0; i < n; i++)
        dst[i] = src[i];
}

void s_des_s_box(const bit src[4], bit dst[2], uint8_t s_box[4][4])
{
    bit src_row[2] = {src[0], src[3]};
    uint8_t row = bit_arr_to_num(2, src_row);

    bit src_col[2] = {src[1], src[2]};
    uint8_t col = bit_arr_to_num(2, src_col);

    bit_arr_from_num(2, s_box[row][col], dst);
}

void s_des_key_gen(int i, bit p10_key[10], bit p8_shifted_key[8], uint8_t p8[8])
{
    bit left[5], right[5];
    bit_arr_split_half(10, p10_key, left, right);

    bit shifted_left[5], shifted_right[5];
    bit_arr_left_shift(5, i, left, shifted_left);
    bit_arr_left_shift(5, i, right, shifted_right);

    bit combine[10];
    bit_arr_combine(10, shifted_left, shifted_right, combine);
    bit_arr_permute_by_map(10, 8, combine, p8_shifted_key, p8);
}

void s_des_encryption(const uint8_t rounds, const bit plain_text[8], const bit key[10], bit encrypted_text[8], uint8_t ip[8], uint8_t p10[10], uint8_t p8[8], uint8_t p4[4], uint8_t ep[8], uint8_t s0[4][4], uint8_t s1[4][4])
{
    bit ip_plain_text[8];
    bit_arr_permute_by_map(8, 8, plain_text, ip_plain_text, ip);

    bit left[4], right[4];
    bit_arr_split_half(8, ip_plain_text, left, right);

    bit p10_key[10];
    bit_arr_permute_by_map(10, 10, key, p10_key, p10);

    for (int r = 1; r <= rounds; r++)
    {
        bit ep_right[8];
        bit_arr_permute_by_map(4, 8, right, ep_right, ep);

        bit k[8];
        s_des_key_gen(2 * r - 1, p10_key, k, p8);

        bit ep_right_xor_k[8];
        bit_arr_xor(8, ep_right, k, ep_right_xor_k);

        bit ep_right_xor_k_left[4], ep_right_xor_k_right[4];
        bit_arr_split_half(8, ep_right_xor_k, ep_right_xor_k_left, ep_right_xor_k_right);

        bit s_boxies[4];
        bit s0_res[2];
        bit s1_res[2];
        s_des_s_box(ep_right_xor_k_left, s0_res, s0);
        s_des_s_box(ep_right_xor_k_right, s1_res, s1);
        bit_arr_combine(4, s0_res, s1_res, s_boxies);

        bit p4_s_boxes[4];
        bit_arr_permute_by_map(4, 4, s_boxies, p4_s_boxes, p4);

        bit left_xor_p4_sboxes[4];
        bit_arr_xor(4, left, p4_s_boxes, left_xor_p4_sboxes);

        bit_arr_copy(4, right, left);
        bit_arr_copy(4, left_xor_p4_sboxes, right);
    }

    bit combine[8];
    bit_arr_combine(8, right, left, combine);
    uint8_t inv_ip[8];
    uint8_arr_invert_of_permutation(8, ip, inv_ip);
    bit_arr_permute_by_map(8, 8, combine, encrypted_text, inv_ip);
}

void s_des_decryption(const uint8_t rounds, const bit encrypted_text[8], const bit key[10], bit decrypted_text[8], uint8_t ip[8], uint8_t p10[10], uint8_t p8[8], uint8_t p4[4], uint8_t ep[8], uint8_t s0[4][4], uint8_t s1[4][4])
{
    bit ip_encrypted_text[8];
    bit_arr_permute_by_map(8, 8, encrypted_text, ip_encrypted_text, ip);

    bit left[4], right[4];
    bit_arr_split_half(8, ip_encrypted_text, left, right);

    bit p10_key[10];
    bit_arr_permute_by_map(10, 10, key, p10_key, p10);

    for (int r = rounds; r >= 1; r--)
    {
        bit ep_right[8];
        bit_arr_permute_by_map(4, 8, right, ep_right, ep);

        bit k[8];
        s_des_key_gen(2 * r - 1, p10_key, k, p8);

        bit ep_right_xor_k[8];
        bit_arr_xor(8, ep_right, k, ep_right_xor_k);

        bit ep_right_xor_k_left[4], ep_right_xor_k_right[4];
        bit_arr_split_half(8, ep_right_xor_k, ep_right_xor_k_left, ep_right_xor_k_right);

        bit s_boxies[4];
        bit s0_res[2];
        bit s1_res[2];
        s_des_s_box(ep_right_xor_k_left, s0_res, s0);
        s_des_s_box(ep_right_xor_k_right, s1_res, s1);
        bit_arr_combine(4, s0_res, s1_res, s_boxies);

        bit p4_s_boxes[4];
        bit_arr_permute_by_map(4, 4, s_boxies, p4_s_boxes, p4);

        bit left_xor_p4_sboxes[4];
        bit_arr_xor(4, left, p4_s_boxes, left_xor_p4_sboxes);

        bit_arr_copy(4, right, left);
        bit_arr_copy(4, left_xor_p4_sboxes, right);
    }

    bit combine[8];
    bit_arr_combine(8, right, left, combine);
    uint8_t inv_ip[8];
    uint8_arr_invert_of_permutation(8, ip, inv_ip);
    bit_arr_permute_by_map(8, 8, combine, decrypted_text, inv_ip);
}

int main()
{
    uint8_t p10[10] = {3, 5, 2, 7, 4, 10, 1, 9, 8, 6};
    uint8_t p8[8] = {6, 3, 7, 4, 8, 5, 10, 9};
    uint8_t p4[4] = {2, 4, 3, 1};
    uint8_t ep[8] = {4, 1, 2, 3, 2, 3, 4, 1};
    uint8_t ip[8] = {2, 6, 3, 1, 4, 8, 5, 7};
    uint8_t s0[4][4] = {{1, 0, 3, 2}, {3, 2, 1, 0}, {0, 2, 1, 3}, {3, 1, 3, 2}};
    uint8_t s1[4][4] = {{0, 1, 2, 3}, {2, 0, 1, 3}, {3, 0, 1, 0}, {2, 1, 0, 3}};

    bit key[10] = "1100011110";

    char k[10];
    printf("k = ");
    scanf("%s", k);
    printf("%s", "plain_text = ");
    char buffer[MAX_BUFFER_SIZE];
    scanf("%s", buffer);
    int n = strlen(buffer);
    int m = (n / 8) + ((n % 8) != 0);
    bit plain_text[m][8];
    for (int i = 0, j = 0, k = 0; i < n; i++)
    {
        plain_text[j][k++] = buffer[i];
        if (k == 7)
        {
            j++;
            k = 0;
        }
    }
    if (n % 8 != 0)
        for (int i = n % 8; i < 8; i++)
            plain_text[m - 1][i] = bit_parse(0);

    bit encrypted_text[m][8];
    bit decrypted_text[m][8];

    for (int i = 0; i < m; i++)
    {
        s_des_encryption(2, plain_text[i], key, encrypted_text[i], ip, p10, p8, p4, ep, s0, s1);
        s_des_decryption(2, encrypted_text[i], key, decrypted_text[i], ip, p10, p8, p4, ep, s0, s1);
    }

    printf("\nencrypted_text = ");
    for (int i = 0; i < m; i++)
        bit_arr_print(8, encrypted_text[i]);

    printf("\ndecrypted_text = ");
    for (int i = 0; i < m; i++)
        bit_arr_print(8, decrypted_text[i]);

    printf("\n");
    return 0;
}
