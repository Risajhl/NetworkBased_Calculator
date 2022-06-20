from socket import *


def main():
    host = "localhost"
    port = 8000
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))  # Bind to the port
    server_socket.listen(1)
    number_1 = "none"
    number_2 = "none"
    operator = "none"
    started = False

    while True:
        print("********")
        c, addr = server_socket.accept()  # Establish connection with client.
        print("connection:", c)
        print('Got connection from', addr)
        while True:
            request = c.recv(1024).decode()
            print("request is: ", request)

            if request == "start":
                started = True
                c.send("OK".encode())


            elif request == "exit":
                started = False
                number_1 = "none"
                number_2 = "none"
                operator = "none"

                c.send("Exit".encode())
                c.close()
                break

            else:
                if started:

                    if number_1 == "none":
                        number_1 = request
                        c.send("GotFirst".encode())
                    elif number_2 == "none":
                        number_2 = request
                        c.send("GotSecond".encode())
                    elif operator == "none":
                        operator = request
                        print(number_1, number_2, operator)
                        check(c, number_1, number_2, operator)
                        number_1 = "none"
                        number_2 = "none"
                        operator = "none"

                else:
                    c.send("Invalid".encode())

        print("out of while")
        c.close()


def check(c, number_1, number_2, operator):
    print("number_1: ", number_1)
    print("number_2: ", number_2)
    print("operation: ", operator)

    try:

        number_1 = float(number_1)
        number_2 = float(number_2)
        if operator != "+" and operator != "-" and operator != "/" and operator != "*":
            c.send("OperationError".encode())
        else:
            calculate(c, number_1, number_2, operator)

    except (ValueError):
        c.send("ValueError".encode())


def calculate(c, number_1, number_2, operator):
         try:
             answer = str(number_1) + operator + str(number_2) + " = "
             result = 0
             if operator == "+":
                  result = (number_1 + number_2)
             elif operator == "-":
                  result = (number_1 - number_2)
             elif operator == "/":
                  result = (number_1 / number_2)
             elif operator == "*":
                  result = (number_1 * number_2)

             final_answer = answer + str(result)
             c.send(final_answer.encode())

         except (ZeroDivisionError):
             c.send("ZeroDiv".encode())
         except (ArithmeticError):
             c.send("MathError".encode())
         except (SyntaxError):
             c.send("SyntaxError".encode())
         except (NameError):
             c.send("NameError".encode())

if __name__ == '__main__':
    main()
