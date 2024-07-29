from typing import List

class HillCipher:
    def __init__(self, key, n) -> None:
        self.n = n
        self.key_matrix = self._get_key_matrix(key, n)
        self.inverse_key_matrix = self._get_inverse_matrix(self.key_matrix) 
    
    def _get_inverse_matrix(self, matrix):
        n = len(matrix)
        det_inverse_matrix = pow(self._get_determine_matrix(matrix), -1, 26)
        adjoint_matrix = self._get_adjoint_matrix(matrix)
        inverse_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                inverse_matrix[i][j] = (adjoint_matrix[i][j] * det_inverse_matrix) % 26
        return inverse_matrix
        

    def _get_adjoint_matrix(self, matrix):
        n = len(matrix)
        adjoint_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                adjoint_matrix[j][i] = ((-1) ** (i + j)) * self._get_minor(matrix, i, j)
        return adjoint_matrix
                
    
    def _get_minor(self, matrix, i, j) -> int:
        n = len(matrix)
        minor_matrix = [[0] * (n-1) for _ in range(n-1)]
        p, q = 0, 0
        for k in range(n):
            for l in range(n):
                if k == i or l == j:
                    continue
                minor_matrix[p][q] = matrix[k][l]
                if q == (n-1):
                    q = 0
                    p += 1
        return self._get_determine_matrix(minor_matrix)


    def _get_determine_matrix(self, matrix: List[List[int]]) -> int:
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for i in range(n):
            det += matrix[i][0] * ((-1) ** i) * self._get_minor(matrix, i, 0)
        return det
    
    def _mul_number_matrix(self, matrix, num):
        n = len(matrix)
        output = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                output[i][j] = num * matrix[i][j]
        return output

    def decrypt(self, encrypted):
        if len(encrypted) % self.n != 0:
            raise Exception("message length error")
        m = len(encrypted) // self.n
        plain_matrix = [[0] * m for _ in range(self.n)]
        encrypted_vector = self._get_message_vector(encrypted, m)
        for i in range(self.n):
            for j in range(m):
                plain_matrix[i][j] = 0
                for x in range(self.n):
                    plain_matrix[i][j] += (self.inverse_key_matrix[i][x] * encrypted_vector[x][j])
                plain_matrix[i][j] %= 26
        plain_text = []
        for i in range(m):
            for j in range(self.n):
                plain_text.append(chr(plain_matrix[j][i] + 65))
        return "".join(plain_text)
        

    def encrypt(self, message):
        if len(message) % self.n != 0:
            raise Exception("message length error")
        m = len(message) // self.n
        cipher_matrix = [[0] * m for _ in range(self.n)]
        message_vector = self._get_message_vector(message, m)
        for i in range(self.n):
            for j in range(m):
                cipher_matrix[i][j] = 0
                for x in range(self.n):
                    cipher_matrix[i][j] += (self.key_matrix[i][x] * message_vector[x][j])
                cipher_matrix[i][j] %= 26
        cipher_text = []
        for i in range(m):
            for j in range(self.n):
                cipher_text.append(chr(cipher_matrix[j][i] + 65))
        return "".join(cipher_text)

    def _get_message_vector(self, message, m):
        message_vector = [[0] * m for _ in range(self.n)]
        for i in range(self.n):
            for j in range(m):
                message_vector[i][j] = ord(message[self.n*j + i]) % 65
        return message_vector

    def _get_key_matrix(self, key, n):
        key_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
               key_matrix[i][j] = ord(key[i*n + j]) % 65
        return key_matrix

def main():
    key = "BEAF"
    cipher = HillCipher(key, 2)
    encrypted = cipher.encrypt(message="HODAEE")
    print("Key = ", key)
    print("Cipher Message = ", encrypted)
    print("Plain Message = ", cipher.decrypt(encrypted))
 
if __name__ == "__main__":
    main()
