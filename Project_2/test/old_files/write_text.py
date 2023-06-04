def main():
    TAB = '\t'
    ENTER = '\n'
    
    with open('test.txt', 'w') as f:
        f.write('Hello, world!' + ENTER)
        f.write(TAB + 'This is a tab.' + ENTER)
        f.write(ENTER + 'This is a new line.')



if __name__ == '__main__':
    main()