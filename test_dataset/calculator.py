def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

def main():
    print("Testing Calculator...")
    print(add(2, 3))
    print(divide(10, 2))

if __name__ == "__main__":
    main()