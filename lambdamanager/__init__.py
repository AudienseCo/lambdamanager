from lambdamanager.maincommand import LambdaManagerCommand


def main():
    """
    The entrypoint to main script
    """
    LambdaManagerCommand()()
    print("This is the entry point to main script")


if __name__ == '__main__':
    main()
