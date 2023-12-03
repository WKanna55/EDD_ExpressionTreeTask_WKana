import re
# ejemplo para "3 + (4 * 5)"

class ExpressionTree:
    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    def tokenize_expression(self, expression):
        # Quita los espacios de la expresion
        expression = expression.replace(" ", "")

        # Usa expresiones regulares para tokenizar la expresion
        tokens = re.findall(r"\d+|[()+\-*/]", expression)

        # manejo de excepciones con expresiones irregulares en cuanto a parentesis
        pila = [] # seguimiento de parentesis
        for token in tokens: # iterar en los tokens
            if token == "(": # si encuentra una parentesis abierto "(" se agrega a la pila de seguimiento
                pila.append(token)
            elif token == ")": # si encuentra una parentesis cerrado ")" se eliminar de la pila de seguimiento el ultimo valor
                if len(pila) == 0: # si no hay nada que eliminar
                    raise Exception("Error: la expresion tiene parentesis en orden incorrecto")
                pila.pop()
        if len(pila) != 0: # si la pila de seguimiento se quedo con algun parentesis
            raise Exception("Error: la expresion tiene parentesis en orden incorrecto")

        return tokens   # retorna ["3", "+", "(", "4", "*", "5", ")"]

    def is_operator(self, token):
        return token in "+-*/"

    def precedence(self, operator):
        if operator in "+-":
            return 1
        if operator in "*/":
            return 2
        return 0

    def infix_to_postfix(self, expression):
        output = []           # Lista para almacenar la expresión en notación postfija
        operator_stack = []   # Pila para almacenar operadores y paréntesis temporales
        
        for token in expression:
            if token.isdigit():
                output.append(token)  # Agregar operandos directamente a la salida
            elif token == "(":
                operator_stack.append(token)  # Empujar paréntesis izquierdo a la pila
            elif token == ")":
                # Sacar operadores de la pila hasta encontrar el paréntesis izquierdo correspondiente
                while operator_stack and operator_stack[-1] != "(":
                    output.append(operator_stack.pop())
                operator_stack.pop()  # Sacar el paréntesis izquierdo de la pila
            elif self.is_operator(token):
                # Sacar operadores de la pila mientras tengan mayor o igual precedencia
                while operator_stack and self.is_operator(operator_stack[-1]) and self.precedence(operator_stack[-1]) >= self.precedence(token):
                    output.append(operator_stack.pop())
                operator_stack.append(token)  # Empujar el operador actual a la pila
        
        # Sacar cualquier operador restante de la pila y agregarlo a la salida
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output     # retorna ["3", "4", "5", "*", "+"] <-> postfix

    def build_expression_tree(self, postfix):
        # Implementar metodo aqui
        stack = [] # pila de seguimiento para operadores y operandos

        for token in postfix:
            if token.isdigit(): # si es un numero ingresar nodo a la pila
                node = self.Node(token) # crear nodo
                stack.append(node) # ingresar nodo a la pila

            elif self.is_operator(token): # si es operador sacar 2 hijos de la pila y añadireselo, luego agregar a pila
                operator_node = self.Node(token) # crear nodo operador
                operator_node.right = stack.pop() # asignar hijos derecho e izquierdo
                operator_node.left = stack.pop()
                stack.append(operator_node) # agregar el nodo a la pila
        return stack.pop() # devolver raiz


    def evaluate_expression_tree(self, root):
        # Implementar metodo aqui
        if root.value.isdigit(): # si es operando retornar valor numerico
            return int(root.value)
        if self.is_operator(root.value): # si es operador retornar la expresion aritmetica segun operador recursivamente
            if root.value == "+":
                return self.evaluate_expression_tree(root.left) + self.evaluate_expression_tree(root.right)
            elif root.value == "-":
                return self.evaluate_expression_tree(root.left) - self.evaluate_expression_tree(root.right)
            elif root.value == "/":
                return self.evaluate_expression_tree(root.left) / self.evaluate_expression_tree(root.right)
            elif root.value == "*":
                return self.evaluate_expression_tree(root.left) * self.evaluate_expression_tree(root.right)


tree = ExpressionTree()  
expression = "3 +    ( 4  * 5 )"
tokens = tree.tokenize_expression(expression)
postfix = tree.infix_to_postfix(tokens)
root = tree.build_expression_tree(postfix)
result = tree.evaluate_expression_tree(root)
print(f"Expression Tree Evaluation: {expression.replace(' ', '')} = {result}")