WRITTEN_DIGETS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
WRITTEN_DIGETS_TO_ASCII = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

class Solution:
    @staticmethod
    def findCalibrationValue(input):
        calibrationValue = 0
        for i in range(len(input)):
            value = Solution.findNumber(input[i])
            print('Cvalue: {}, line: {}\n'.format(value, input[i]))
            calibrationValue += value
        return calibrationValue
    
    @staticmethod
    def findNumber(line):
        result = ''
        i = 0
        while i < len(line):
            firstNumber = ''
            if Solution.isNumber(line[i]):
                firstNumber = line[i]
            else:
                for digit in WRITTEN_DIGETS:
                    if line[i:].startswith(digit):
                        firstNumber = WRITTEN_DIGETS_TO_ASCII[digit]
                        break

            if firstNumber != '':
                result += firstNumber
                break
            i += 1

        lastNumber = ''
        while i < len(line):
            if Solution.isNumber(line[i]):
                lastNumber = line[i]
            else:
                for digit in WRITTEN_DIGETS:
                    if line[i:].startswith(digit):
                        lastNumber = WRITTEN_DIGETS_TO_ASCII[digit]
                        break
            i += 1
        return int(result + lastNumber)

    @staticmethod
    def isNumber(char):
        if ord(char) >= 48 and ord(char) <= 57:
            return True
        return False


if __name__ == '__main__':
    with open('input1.txt', 'r') as reader:
        input = reader.readlines()
        # print('number = {}'.format(Solution.findNumber('tw1')))
        print('Calibration value: {}'.format(Solution.findCalibrationValue(input)))
        #print('fix input: {}'.format(Solution.fixInput(input)))