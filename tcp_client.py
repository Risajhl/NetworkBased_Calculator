from socket import *

error = False
exit = False


def main():
    global error
    global exit
    host = "localhost"
    port = 8000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))
    print("The IP address of the server is:", host)
    print("The port number of the server is:", port)

    while (True):
        print("Waiting... (start / exit)")

        request = input()
        clientSocket.send(request.encode())
        answer = clientSocket.recv(1024).decode()
        if answer == "OK":
            print("Enter first number:")
            start_calculating(clientSocket)
            if error:
                continue
            if exit:
                break

        if answer == "Exit":
            print("Closing client")
            break

        if answer == "Invalid":
            print("Invalid")


def start_calculating(clientSocket):
    global error
    global exit
    while True:
        data = input()
        clientSocket.send(data.encode())
        result = clientSocket.recv(1024).decode()

        if result == "Exit":
            print("Closing client")
            exit = True
            break

        elif result == "ZeroDiv":
            error = True
            print("You can't divide by 0")
            break
        elif result == "MathError":
            error = True
            print("There is an error with your math")
            break
        elif result == "SyntaxError":
            error = True
            print("There is a syntax error")
            break
        elif result == "NameError":
            error = True
            print("You did not enter an equation")
            break
        elif result == "ValueError":
            error = True
            print("One of the entered numbers are invalid")
            break
        elif result == "OperationError":
            error = True
            print("Operation is invalid")
            break

        elif result == "GotFirst":
            print("Enter second number:")
        elif result == "GotSecond":
            print("Enter operator:")

        else:
            print("The answer is:", result, "\nEnter first number:")

    clientSocket.close  # Close the socket when done


if __name__ == '__main__':
    main()
