from functools import total_ordering

@total_ordering
class CustomNumber:
    def __init__(self, value):
        if value.startswith('-'):
            self.sign = -1
            value = value[1:]
        else:
            self.sign = 1

        self.digits = []
        for d in reversed(value):
            self.digits.append(int(d))

        self.length = len(self.digits)

    def __str__(self):
        return ('-' if self.sign < 0 else '') + ''.join(map(str, self.digits[::-1]))
    
    def __add__(self, other):
        if self.sign == other.sign:
            result_digits = []
            temp = 0
            for i in range(max(self.length, other.length)):
                d1 = self.digits[i] if i < self.length else 0
                d2 = other.digits[i] if i < other.length else 0
                total = d1 + d2 + temp
                result_digits.append(total % 10)
                temp = total // 10
            if temp:
                result_digits.append(temp)

            res = CustomNumber("0")
            res.sign = self.sign
            res.digits = result_digits
            res.length = len(result_digits)
            return res
        else:
            if self.sign < 0:
                return other - CustomNumber(str(self)[1:])
            else:
                return self - CustomNumber(str(other)[1:])
        
    def __sub__(self, other):
        if self < other:
            res = other - self
            res.sign = -1
            return res
        
        result_digits = []
        temp = 0
        for i in range(self.length):
            d1 = self.digits[i]
            d2 = other.digits[i] if i < other.length else 0
            total = d1 - d2 - temp
            if total < 0:
                total += 10
                temp = 1
            else:
                temp = 0
            result_digits.append(total)

        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        res = CustomNumber("0")
        res.sign = 1
        res.digits = result_digits
        res.length = len(result_digits)
        return res
        
    def __mul__(self, other):
        result_digits = [0] * (self.length + other.length)

        for i in range(self.length):
            temp = 0
            for j in range(other.length):
                total = self.digits[i] * other.digits[j] + result_digits[i + j] + temp
                result_digits[i + j] = total % 10
                temp = total // 10
            if temp > 0:
                result_digits[i + other.length] += temp

        while len(result_digits) > 1 and result_digits[-1] == 0:
            result_digits.pop()

        res = CustomNumber("0")
        res.sign = self.sign * other.sign
        res.digits = result_digits
        res.length = len(result_digits)
        return res
    
    def __floordiv__(self, other):
        if other.length == 1 and other.digits[0] == 0:
            raise ZeroDivisionError("Division by zero")
        
        dividend = abs(self)
        divisor = abs(other)
        
        result_digits = []
        remainder = CustomNumber("0")

        for i in range(dividend.length - 1, -1, -1):
            remainder.digits.insert(0, dividend.digits[i])
            remainder.strip_leading_zeros()

            count = 0
            while remainder >= divisor:
                remainder = remainder - divisor
                count += 1
            result_digits.insert(0, count)

        res = CustomNumber("0")
        res.sign = self.sign * other.sign
        res.digits = result_digits
        res.strip_leading_zeros()
        res.length = len(res.digits)
        
        return res
    
    def to_decimal(self):
        return str(self)
    
    def to_binary(self):
        if self.length == 1 and self.digits[0] == 0:
            return "0"
        
        temp = CustomNumber(str(self))
        result_digits = []

        base = CustomNumber("2")
        while temp.length > 1 or temp.digits[0] != 0:
            remainder = temp % base
            result_digits.append(str(remainder.digits[0]))
            temp = temp // base

        result_digits.reverse()
        return ('-' if self.sign < 0 else '') + ''.join(result_digits)

    def strip_leading_zeros(self):
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()
        self.length = len(self.digits)

    def __lt__(self, other):
        if self.sign != other.sign:
            return self.sign < other.sign
        
        if self.sign > 0:
            if self.length != other.length:
                return self.length < other.length
            
            for i in range(self.length - 1, -1, -1):
                if self.digits[i] != other.digits[i]:
                    return self.digits[i] < other.digits[i]
            return False        
        else:
            if self.length != other.length:
                return self.length > other.length
            for i in range(self.length - 1, -1, -1):
                if self.digits[i] != other.digits[i]:
                    return self.digits[i] > other.digits[i]
            return False
        
    def __eq__(self, other):
        return self.sign == other.sign and self.digits == other.digits
    
    def __abs__(self):
        res = CustomNumber("0")
        res.digits = self.digits.copy()
        res.sign = 1
        res.length = self.length
        return res
        
    def __mod__(self, other):
        quotient = self // other
        remainder = self - quotient * other
        return remainder
    
# a = CustomNumber("123")
# b = CustomNumber("45")
# c = CustomNumber("-77")
# d = CustomNumber("100")

# print("№ | Decimal numbers | Binary numbers")
# print(f"a | {a.to_decimal()} | {a.to_binary()}")
# print(f"b | {b.to_decimal()} | {b.to_binary()}")
# print(f"c | {c.to_decimal()} | {c.to_binary()}")
# print(f"d | {d.to_decimal()} | {d.to_binary()}")
# print()

# print("Arithmetic")
# print("a + b = ", (a + b).to_decimal())
# print("a + c = ", (a + c).to_decimal())
# print("a - b = ", (a - b).to_decimal())
# print("b - a = ", (b - a).to_decimal())
# print("a * b = ", (a * b).to_decimal())
# print("d // b = ", (d // b).to_decimal())
# print("d % b = ", (d % b).to_decimal())

a = CustomNumber("-77")
b = CustomNumber("2")
c = CustomNumber("-38")
print("-77 // 2 = ", (a // b).to_decimal())
print("-38 * 2 = ", (c * b).to_decimal())
d = CustomNumber((c * b).to_decimal())
print("-77 - (-38 * 2) = ", (a - d).to_decimal())