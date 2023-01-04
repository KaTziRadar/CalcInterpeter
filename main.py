from functools import reduce
from operator import mul

known_operators = ['add', 'sub', 'mul', 'div','+', '+', '*', '/']
class Exp(object):
    """A call expression in Calculator."""
    def __init__(self, operator, operands):
     self.operator = operator
     self.operands = operands
    def __repr__(self):
     return 'Exp({0},{1})'.format(repr(self.operator),repr(self.operands))
    def __str__(self):
     operand_strs = ','.joint(map(str,self.operands))
     return '{0}({1})'.format(self.operator, operand_strs)
    def calc_eval(self,exp):
     """Evaluate a Calculator expression."""
     if type(exp) in (int, float):
         return exp
     elif type(exp) == Exp:
        arguments = list(map(lambda y: self.calc_eval(self,y),exp.operands))
        return self.calc_apply(self,exp.operator, arguments)
    def calc_apply(self,operator, args):
        """Apply the named operator to a list of args."""
        if operator in ('add','+'):
            return sum(args)
        if operator in ('sub', '-'):
         if len(args) == 0:
            raise TypeError(operator + 'requires  at  least 1 argument')
         if len(args) == 1:
            return -args[0]
         return sum(args[:1] + [-arg for arg in args[1:]])
        if operator in ('mul', '*'  ):
         return reduce(mul , args, 1)
        if operator in ('div', '/' ):
            if len(args) != 2:
                raise TypeError(operator + 'requiresexactly  2 arguments')
            numer, denom = args
            return numer / denom
    def read_eval_print_loop(self):
     """Run a read-eval-print loop for calculator."""
     while True:
      try:
            expression_tree = self.calc_parse(self,input('calc>'))
            print(self.calc_eval(self,expression_tree))
      except (SyntaxError, TypeError, ZeroDivisionError) as err:
        print(type(err).__name__ + ':',err)
      except (KeyboardInterrupt, EOFError): # <Control>-D, etc.
          print('Calculation completed.')
          return
    def tokenize(self,line):
        """Convert a string into a list of tokens."""
        spaced = line.replace('(',' ( ').replace(')',' ) ').replace(',', ' , ')
        return spaced.split()
    def analyze(self,tokens):
          """Create a tree of nested lists from a sequence of tokens."""
          self.assert_non_empty(self,tokens)
          token = self.analyze_token(self,tokens.pop(0))
          if type(token) in (int, float):
           return token
          if token in known_operators:
            if len(tokens) == 0 or tokens.pop(0) != '(':
                 raise SyntaxError('expected(after ' + token)
            return Exp(token, self.analyze_operands(self,tokens))
          else:
            raise SyntaxError('unexpected ' + token)
    def analyze_operands(self,tokens):
        """Analyze a sequence of comma-separated operands."""
        self.assert_non_empty(self,tokens)
        operands = []
        while tokens[0] != ')':
            if operands and tokens.pop(0) != ',':
                raise SyntaxError('expected,')
            operands.append(self.analyze(self,tokens))
            self.assert_non_empty(self,tokens)
        tokens.pop(0)  # Remove )
        return operands
    def analyze_token(self,token):
        """Return the value of token if it can be analyzed as a number, or token."""
        try:
            return int(token)
        except (TypeError, ValueError):
         try:
            return float(token)
         except (TypeError, ValueError):
            return token
    def assert_non_empty(self,tokens):
        """Raise an exception if tokens is empty."""
        if len(tokens) == 0:
         raise SyntaxError('unexpected end of line')
    def calc_parse(self,line):
        """Parse a line of calculator input and return an expression tree."""
        tokens = self.tokenize(self,line)
        expression_tree = self.analyze(self,tokens)
        print(tokens)
        if len(tokens) > 0:
            raise SyntaxError('Extra  token(s): ' + ' ' .join(tokens))
        return expression_tree
    def fun(self):
        print(self.tokenize(self,"4 + 5"))
Exp.read_eval_print_loop(Exp)






