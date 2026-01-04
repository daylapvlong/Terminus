import sys

def process(data):
    return data[0] + list(data)

def main():
    data = sys.stdin.read()
    result = process(data.strip())
    print(result)

if __name__ == "__main__":
    main()