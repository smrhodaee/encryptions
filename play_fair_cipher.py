from typing import List, Tuple
import sys


def search(matrix, ch) -> Tuple[int, int]:
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == ch:
                return i, j
    return (-1, -1)


class PlaufairCipher:
    def __init__(self, key) -> None:
        alphabets = "abcdefghiklmnopqrstuvwxyz"
        self.key_table = self._get_key_table(key, alphabets)

    def encrypt(self, text: str) -> str:
        return self._execute(text, False)

    def decrypt(self, encrypted: str) -> str:
        return self._execute(encrypted, True)

    def _get_text_normalize(self, text) -> str:
        return text.lower().replace(" ", "").replace("j", "i")

    def _execute(self, inp: str, reverse: bool) -> str:
        inp_list = self._get_diagraph(inp)
        out = ""
        for i in range(len(inp_list)):
            pos = self._get_pos(inp_list, i)
            if pos[0] == pos[2]:
                out += self._row_rule(pos, reverse)
            elif pos[1] == pos[3]:
                out += self._column_rule(pos, reverse)
            else:
                out += self._rectangle_rule(pos)
        return out

    def _row_rule(self, pos, reverse) -> str:
        out = ""
        if reverse:
            for j in range(2):
                if pos[2 * j + 1] == 0:
                    out += self.key_table[pos[2 * j]][4]
                else:
                    out += self.key_table[pos[2 * j]][pos[2 * j + 1] - 1]
        else:
            for j in range(2):
                if pos[2 * j + 1] == 4:
                    out += self.key_table[pos[2 * j]][0]
                else:
                    out += self.key_table[pos[2 * j]][pos[2 * j + 1] + 1]
        return out

    def _column_rule(self, pos, reverse) -> str:
        out = ""
        if reverse:
            for j in range(2):
                if pos[2 * j] == 0:
                    out += self.key_table[pos[4]][2 * j + 1]
                else:
                    out += self.key_table[pos[2 * j] - 1][pos[2 * j + 1]]
        else:
            for j in range(2):
                if pos[2 * j] == 4:
                    out += self.key_table[pos[0]][2 * j + 1]
                else:
                    out += self.key_table[pos[2 * j] + 1][pos[2 * j + 1]]
        return out

    def _rectangle_rule(self, pos) -> str:
        out = ""
        out += self.key_table[pos[0]][pos[3]]
        out += self.key_table[pos[2]][pos[1]]
        return out

    def _get_pos(self, plain_list, i):
        pos = []
        for j in range(2):
            pos.extend(search(self.key_table, plain_list[i][j]))
        return pos

    def _get_diagraph(self, text: str) -> List[List[str]]:
        output = []
        text = self._get_text_normalize(text)
        n = len(text)
        i = 0
        while i < n:
            pair = []
            pair.append(text[i])
            #if i + 1 == n:
            #    pair.append("z")
            #elif text[i] == text[i + 1]:
            #    pair.append("x")
            #else:
            pair.append(text[i + 1])
            i += 1
            output.append(pair)
            i += 1
        return output

    def _get_key_table(self, key: str, alphabets: str):
        table = [[""] * 5 for _ in range(5)]
        key = self._get_text_normalize(key)
        include = set()
        i, j = 0, 0
        for k in key:
            if k not in include:
                table[i][j] = k
                j += 1
                if j == 5:
                    i += 1
                    j = 0
            include.add(k)
        for ch in alphabets:
            if ch not in include:
                table[i][j] = ch
                j += 1
                if j == 5:
                    i += 1
                    j = 0
            include.add(ch)
        return table


def main():
    if len(sys.argv) < 2:
        print("Usgae: ")
        exit(1)
    key = sys.argv[1]
    text = sys.argv[2]
    cipher = PlaufairCipher(key)
    encrypted = cipher.encrypt(text)
    dectypted = cipher.decrypt(encrypted)
    print("Key = ", key)
    print("Plain Text = ", text)
    print("Encypted Text = ", encrypted)
    print("Decrypted Text = ", dectypted)


if __name__ == "__main__":
    main()
