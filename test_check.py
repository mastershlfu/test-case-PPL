def test_001():
    """Test a valid program that should pass all checks"""
    source = """
    const PI: float = 3.14;
    func main() -> void {
        let x: int = 5;
        let y = x + 1;
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"
    
def test_002():
    """Test Redeclared variable"""
    source = """
    func main() -> void {
        let x: int = 5;
        let x = 1;
    }
    """
    assert Checker(source).check_from_source() == "Redeclared Variable: x"

def test_003():
    """Test Redeclared constant"""
    source = """
    const PI: float = 3.14;
    const PI: float = 10.14;
    func main() -> void {
    }
    """
    assert Checker(source).check_from_source() == "Redeclared Constant: PI"

def test_004():
    """Test Redeclared as a constant"""
    source = """
    func main() -> void {
        let x: int = 5;
        const x = 23;
    }
    """
    assert Checker(source).check_from_source() == "Redeclared Constant: x"

def test_005():
    """Test Redeclared function"""
    source = """
    func foo() -> void {}
    func foo() -> int { return 1; }
    func main() -> void {
    }
    """
    assert Checker(source).check_from_source() == "Redeclared Function: foo"

def test_006():
    """Test shadowing a variable"""
    source = """
    func main() -> void {
        let x = 1;
        if (true) {
            x = 2;
        }
        else {
            x = 0;
        }
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_007():
    """Test shadowing a constant"""
    source = """
    const MAX = 100;
    func main() -> void {
        MAX = 50;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: IdLValue(MAX)"

def test_008():
    """Test shadowing a constant as a variable"""
    source = """
    const MAX = 100;
    func main() -> void {
        let MAX = 13;
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_009():
    """Test Redeclared Parameter"""
    source = """
    func foo(x: int) -> int {
        let x: int = 23;
        return x;    
    }
    
    func main() -> void {  
    }
    """
    assert Checker(source).check_from_source() == "Redeclared Variable: x"
    
def test_010():
    """Test Redeclared variable in a loop"""
    source = """
    func main() -> void {
        let arr: [int; 2] = [1,2];  
        for(i in arr) {
            let i = 5;
        }
    }
    """
    assert Checker(source).check_from_source() == "Redeclared Variable: i"

def test_011():
    """Test Undeclared identifier"""
    source = """
    func main() -> void {  
        let x = y;
    }
    """
    assert Checker(source).check_from_source() == "Undeclared Identifier: y"

def test_012():
    """Test Undeclared function"""
    source = """
    func main() -> void {  
        foo();
    }
    """
    assert Checker(source).check_from_source() == "Undeclared Function: foo"

def test_013():
    """Test using a variable before declaration"""
    source = """
    func main() -> void {  
        let x = y;
        let y = 1;
    }
    """
    assert Checker(source).check_from_source() == "Undeclared Identifier: y"

def test_014():
    """Test using a function before declaration"""
    source = """
    func main() -> void {  
        foo()
        func foo() -> void {return;}
    }
    """
    assert Checker(source).check_from_source() == "Undeclared Function: foo"

def test_015():
    """Test out of scope variable"""
    source = """
    func print(s: string) -> string {
        return s;
    }
    
    func main() -> void {  
        if (true) {
            let s = "hello";
        }
        print(s);
    }
    """
    assert Checker(source).check_from_source() == "Undeclared Identifier: s"

def test_016():
    """Test out of scope function"""
    source = """
    func print(s: string) -> string {
        return s;
    }
    
    func main() -> void {  
        { func foo() -> void {print("hi");} }
        foo();
    }
    """
    assert Checker(source).check_from_source() == "Undeclared Function: foo"

def test_017():
    """Test using constant before declaration"""
    source = """
    func main() -> void {  
        let x = MAX;
    }
    const MAX: int = 100;
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_018():
    """Test invalid index - string index"""
    source = """
    func main() -> void {  
        let number: [int; 4] = [0, 3, 6, 9];
        let result = number["1"];
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: StringLiteral('1')"

def test_019():
    """Test invalid index - float index"""
    source = """
    func main() -> void {  
        let number: [int; 4] = [0, 3, 6, 9];
        let result = number[2.3];
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: FloatLiteral(2.3)"

def test_020():
    """Test invalid index - array index"""
    source = """
    func main() -> void {  
        let number: [int; 4] = [0, 3, 6, 9];
        let string_: [string; 3] = ["P", "P", "L"];
        let result = number[string_];
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: Identifier(string_)"

def test_021():
    """Test invalid index - bool index"""
    source = """
    func main() -> void {  
        let number: [int; 4] = [0, 3, 6, 9];
        let result = number[false];
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: BooleanLiteral(False)"

def test_022():
    """Test Binary operation errors - sum = int + bool"""
    source = """
    func main() -> void {  
        let x = 2;
        let y = true;
        let sum = x + y;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: BinaryOp(Identifier(x), +, Identifier(y))"

def test_023():
    """Test Binary operation errors - sum = int + float"""
    source = """
    func main() -> void {  
        let x = 2;
        let y = 0.3;
        let sum = x + y;
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_024():
    """Test Binary operation errors - sum = string + string"""
    source = """
    func main() -> void {  
        let x = "Hello";
        let y = "World";
        let sum = x + y;
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_025():
    """Test Binary operation errors - comparision: int vs float"""
    source = """
    func main() -> void {  
        let x = 4;
        let y = 5.0;
        let comparision = x > y;
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_026():
    """Test Binary operation errors - comparision: int vs string"""
    source = """
    func main() -> void {  
        let x = 4;
        let y = "hi";
        let comparision = x > y;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: BinaryOp(Identifier(x), >, Identifier(y))"

def test_027():
    """Test Binary operation errors - equality: int vs float"""
    source = """
    func main() -> void {  
        let x = 4;
        let y = 5.0;
        let equality = x == y;
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_028():
    """Test Binary operation errors - equality: int vs string"""
    source = """
    func main() -> void {  
        let x = 4;
        let y = "hi";
        let equality = x != y;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: BinaryOp(Identifier(x), !=, Identifier(y))"

def test_029():
    """Test Binary operation errors - logical: int vs bool"""
    source = """
    func main() -> void {  
        let x = 4;
        let y = true;
        let equality = x && y;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: BinaryOp(Identifier(x), &&, Identifier(y))"

def test_030():
    """Test Binary operation errors - logical: int vs bool"""
    source = """
    func main() -> void {  
        let x = 4;
        let y = false;
        let equality = x || y;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: BinaryOp(Identifier(x), ||, Identifier(y))"

def test_031():
    """Test Binary operation errors - mod: int vs float"""
    source = """
    func main() -> void {  
        let module = 45 % 104;
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_032():
    """Test Unary operation errors - not: int"""
    source = """
    func main() -> void {  
        let x = !4;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: UnaryOp(!, IntegerLiteral(4))"

def test_033():
    """Test Unary operation errors - not: float"""
    source = """
    func main() -> void {  
        let x = !4.3;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: UnaryOp(!, FloatLiteral(4.3))"

def test_034():
    """Test Unary operation errors - sub/plus: bool"""
    source = """
    func main() -> void {  
        let x = -false;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: UnaryOp(-, BooleanLiteral(False))"

def test_035():
    """Test Unary operation errors - sub/plus: string"""
    source = """
    func main() -> void {  
        let x = -"hi";
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: UnaryOp(-, StringLiteral('hi'))"

def test_036():
    """Test Function call - void function"""
    source = """
    func print(s: string) -> void { return; }
    
    func main() -> void {  
        let x = print("hi");
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: VarDecl(x, FunctionCall(Identifier(print), [StringLiteral('hi')]))"

def test_037():
    """Test Function call - wrong args"""
    source = """
    func add(x: int, y: int) -> int { return x + y; }
    
    func main() -> void {  
        let x = add(5, "sh");
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(5), StringLiteral('sh')])"

def test_038():
    """Test Function call - too few args"""
    source = """
    func add(x: int, y: int) -> int { return x + y; }
    
    func main() -> void {  
        let x = add(5);
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(5)])"

def test_039():
    """Test Function call - too many args"""
    source = """
    func add(x: int, y: int) -> int { return x + y; }
    
    func main() -> void {  
        let x = add(5,3,4);
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(5), IntegerLiteral(3), IntegerLiteral(4)])"

def test_040():
    """Test Array type mismatches - int + float"""
    source = """    
    func main() -> void {  
        let number: [int; 2] = [36, 63];
        let float: [float; 2] = [3.6, 6.3];
        let x = number[0] + float[0];
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_041():
    """Test Array type mismatches - int + string"""
    source = """    
    func main() -> void {  
        let number: [int; 2] = [36, 63];
        let string_: [string; 2] = ["3.6", "6.3"];
        let x = number[0] + string_[0];
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: BinaryOp(ArrayAccess(Identifier(number), IntegerLiteral(0)), +, ArrayAccess(Identifier(string_), IntegerLiteral(0)))"

def test_042():
    """Test Nested expression errors - bool index"""
    source = """    
    func main() -> void {  
        let number: [int; 2] = [36, 63];
        let x = number[number[true]];
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: BooleanLiteral(True)"

def test_043():
    """Test Function without return type annotation"""
    source = """   
    func noReturn() -> {let x = 5;} 
    func main() -> void {  
        noReturn();
    }
    """
    assert Checker(source).check_from_source() == "Type Cannot Be Inferred: FuncDecl(noReturn, [], None, [VarDecl(x, IntegerLiteral(5))])"

def test_044():
    """Test Empty array without type annotation"""
    source = """   
    func main() -> void {  
        let arr = [];
        arr[1] = 67;
    }
    """
    assert Checker(source).check_from_source() == "Type Cannot Be Inferred: ArrayLiteral([])"

def test_045():
    """Test Forward reference in initialization"""
    source = """   
    func sub(x: int, y: int) -> int { return x + y; }
    func main() -> void {  
        let sum = sub(x,y);
        let x = 2;
        let y = 5;
    }
    """
    assert Checker(source).check_from_source() == "Undeclared Identifier: x"

def test_046():
    """Test Complex expression without sufficient context"""
    source = """   
    func print(s: string) -> string {
        return s;
    }
    
    func type_list() -> type { 
        let typ = Circle;
    }
    func main() -> void {  
        let typ = type_list();
        print(str(typ));
    }
    """
    assert Checker(source).check_from_source() == "Type Cannot Be Inferred: FuncDecl(type_list, [], None, [VarDecl(typ, Identifier(Circle))])"

def test_047():
    """Test Mixed array elements without clear type"""
    source = """   
    func print(s: string) -> string {
        return s;
    }
    
    func getInt() -> int { 
        return 5;
    }
    
    func getFloat() -> float {
        return 7.7;
    }
    
    func main() -> void {  
        let mix = [getInt(), getFloat()];
        print(str(len(mixed)));
    }
    """
    assert Checker(source).check_from_source() == "Type Cannot Be Inferred: ArrayLiteral([FunctionCall(Identifier(getInt), []), FunctionCall(Identifier(getFloat), [])])"

def test_048():
    """Test Function call without void type"""
    source = """   
    func getInt() -> int { 
        return 5;
    }
    
    func main() -> void {  
        getInt();
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_049():
    """Test Function call: void with return"""
    source = """   
    func foo() -> void { 
        return;
    }
    
    func main() -> void {  
        foo();
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_050():
    """Test Conditional statement errors - int condition"""
    source = """   
    func main() -> void {  
        let x = 5;
        if (x) {
            x = 1;
        }
        else {
            x = 0;
        }
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: IfStmt(condition=Identifier(x), then_stmt=BlockStmt([Assignment(IdLValue(x), IntegerLiteral(1))]), else_stmt=BlockStmt([Assignment(IdLValue(x), IntegerLiteral(0))]))"

def test_051():
    """Test Conditional statement errors - string condition"""
    source = """   
    func main() -> void {  
        let x = "hello";
        if (x) {
            x = "1";
        }
        else {
            x = "0";
        }
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: IfStmt(condition=Identifier(x), then_stmt=BlockStmt([Assignment(IdLValue(x), StringLiteral('1'))]), else_stmt=BlockStmt([Assignment(IdLValue(x), StringLiteral('0'))]))"

def test_052():
    """Test Conditional statement errors - string in logical expression"""
    source = """   
    func main() -> void {  
        let x = "hello";
        let y = 6;
        if (x && y > 5) {
            x = "1";
        }
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: IfStmt(condition=BinaryOp(Identifier(x), &&, BinaryOp(Identifier(y), >, IntegerLiteral(5))), then_stmt=BlockStmt([Assignment(IdLValue(x), StringLiteral('1'))]))"

def test_053():
    """Test Loop statement errors - int condition"""
    source = """   
    func main() -> void {  
        let x = 5;
        while (x) {
            x = 1;
        }
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: WhileStmt(Identifier(x), BlockStmt([Assignment(IdLValue(x), IntegerLiteral(1))]))"

def test_054():
    """Test Loop statement errors - string condition"""
    source = """   
    func main() -> void {  
        let x = "hello";
        while (x) {
            x = "hi";
        }
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: WhileStmt(Identifier(x), BlockStmt([Assignment(IdLValue(x), StringLiteral('hi'))]))"

def test_055():
    """Test Loop statement errors - int is not iterable"""
    source = """   
    func main() -> void {  
        let x = 23;
        for (i in x) {
            let y = 1;
        }
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: ForStmt(i, Identifier(x), BlockStmt([VarDecl(y, IntegerLiteral(1))]))"

def test_056():
    """Test Loop statement errors - string is not iterable"""
    source = """   
    func main() -> void {  
        let x = "hello";
        for (i in x) {
            let y = 1;
        }
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: ForStmt(i, Identifier(x), BlockStmt([VarDecl(y, IntegerLiteral(1))]))"

def test_057():
    """Test Assignment statement errors - int to string"""
    source = """   
    func main() -> void {  
        let x = "hello";
        x = 1;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(IdLValue(x), IntegerLiteral(1))"

def test_058():
    """Test Assignment statement errors - float to bool"""
    source = """   
    func main() -> void {  
        let x = true;
        x = 1.0;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(IdLValue(x), FloatLiteral(1.0))"

def test_059():
    """Test Assignment statement errors - float array to int array"""
    source = """   
    func main() -> void {  
        let number: [int; 2] = [1,2];
        number[1] = 2.3;
    } 
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(number), IntegerLiteral(1)), FloatLiteral(2.3))"

def test_060():
    """Test Assignment statement errors - float to int element"""
    source = """   
    func main() -> void {  
        let number: [int; 2] = [1,2];
        number[1] = 2.3;
    } 
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(number), IntegerLiteral(1)), FloatLiteral(2.3))"

def test_061():
    """Test Assignment statement errors - string to int element"""
    source = """   
    func main() -> void {  
        let number: [int; 2] = [1,2];
        number[1] = "hi";
    } 
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(number), IntegerLiteral(1)), StringLiteral('hi'))"

def test_062():
    """Test Assignment statement errors - float array to int array"""
    source = """   
    func main() -> void {  
        let number: [int; 2] = [1,2];
        number = [1.0, 2.0];
    } 
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(IdLValue(number), ArrayLiteral([FloatLiteral(1.0), FloatLiteral(2.0)]))"

def test_063():
    """Test Constant assignment error"""
    source = """   
    const MAX = 36;
    func main() -> void {
        MAX = 37;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: IdLValue(MAX)"

def test_064():
    """Test Return statement errors - bool to int"""
    source = """   
    func returnInt() -> int {
        return false;
    }
    
    func main() -> void {
        let x = returnInt();
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: ReturnStmt(BooleanLiteral(False))"

def test_065():
    """Test Return statement errors - string to float"""
    source = """   
    func returnFloat() -> float {
        return "hello";
    }
    
    func main() -> void {
        let x = returnFloat();
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: ReturnStmt(StringLiteral('hello'))"

def test_066():
    """Test Return statement errors - string to float"""
    source = """   
    func returnArray() -> [int; 3] {
        return [1.0, 2.0, 3.0];
    }
    
    func main() -> void {
        let x = returnArray();
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: ReturnStmt(ArrayLiteral([FloatLiteral(1.0), FloatLiteral(2.0), FloatLiteral(3.0)]))"

def test_067():
    """Test Return statement errors - int to void"""
    source = """   
    func returnVoid() -> void {
        return 36;
    }
    
    func main() -> void {
        returnVoid();
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(36))"

def test_068():
    """Test Function call statement errors - void function assigned to variable"""
    source = """   
    func returnVoid() -> void {
        return;
    }
    
    func main() -> void {
        let x = 0;
        x = returnVoid();
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(IdLValue(x), FunctionCall(Identifier(returnVoid), []))"

def test_069():
    """Test Function call statement errors - string args to int params"""
    source = """   
    func add(x: int, y: int) -> int {
        return x + y;
    }
    
    func main() -> void {
        let a = add("1", "3");
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: FunctionCall(Identifier(add), [StringLiteral('1'), StringLiteral('3')])"

def test_070():
    """Test Function call statement errors - string args to int params"""
    source = """   
    func add(x: int, y: int) -> int {
        return x + y;
    }
    
    func main() -> void {
        add("1", "3");
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: FunctionCall(Identifier(add), [StringLiteral('1'), StringLiteral('3')])"
def test_071():
    """Test Function call statement errors - too few args"""
    source = """   
    func add(x: int, y: int) -> int {
        return x + y;
    }
    
    func main() -> void {
        add(1);
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: FunctionCall(Identifier(add), [IntegerLiteral(1)])"

def test_072():
    """Test Function call errors - too many args"""
    source = """   
    func add(x: int, y: int) -> int {
        return x + y;
    }
    
    func main() -> void {
        let x = 3 >> add(1,2);
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(1), IntegerLiteral(2)])"

def test_073():
    """Test Complex type mismatch errors - different element types"""
    source = """   
    func main() -> void {
        let matrix: [[int; 2]; 2] = [[1, 2], [3, 4]];
        let floatMatrix: [[float; 2]; 2] = [[1.0, 2.0], [3.0, 4.0]]
        
        matrix = floatMatrix;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(IdLValue(matrix), Identifier(floatMatrix))"

def test_074():
    """Test Complex type mismatch errors - float array to int array row"""
    source = """   
    func main() -> void {
        let matrix: [[int; 2]; 2] = [[1, 2], [3, 4]];
        let floatMatrix: [[float; 2]; 2] = [[1.0, 2.0], [3.0, 4.0]]
        
        matrix[0] = [1.0, 2.0];
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(matrix), IntegerLiteral(0)), ArrayLiteral([FloatLiteral(1.0), FloatLiteral(2.0)]))"

def test_075():
    """Test Complex type mismatch errors - float to int element"""
    source = """   
    func main() -> void {
        let matrix: [[int; 2]; 2] = [[1, 2], [3, 4]];
        let floatMatrix: [[float; 2]; 2] = [[1.0, 2.0], [3.0, 4.0]]
        
        matrix[0][0] = 3.14;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(ArrayAccessLValue(ArrayAccess(Identifier(matrix), IntegerLiteral(0)), IntegerLiteral(0)), FloatLiteral(3.14))"

def test_076():
    """Test Complex type mismatch errors - float row index"""
    source = """   
    func main() -> void {
        let matrix: [[int; 2]; 2] = [[1, 2], [3, 4]];
        let floatMatrix: [[float; 2]; 2] = [[1.0, 2.0], [3.0, 4.0]]
        
        matrix[3.14][0] = 0;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: ArrayAccess(Identifier(matrix), FloatLiteral(3.14))"

def test_077():
    """Test Complex type mismatch errors - float column index"""
    source = """   
    func main() -> void {
        let matrix: [[int; 2]; 2] = [[1, 2], [3, 4]];
        let floatMatrix: [[float; 2]; 2] = [[1.0, 2.0], [3.0, 4.0]]
        
        matrix[0][3.14] = 0;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(ArrayAccessLValue(ArrayAccess(Identifier(matrix), IntegerLiteral(0)), FloatLiteral(3.14)), IntegerLiteral(0))"

def test_078():
    """Test Array size mismatch - large to small"""
    source = """   
    func main() -> void {
        let small: [int; 2] = [1, 2];
        let large: [int; 4] = [1,2,3,4];
        
        small = large;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(IdLValue(small), Identifier(large))"
    
def test_079():
    """Test Array size mismatch - small to large"""
    source = """   
    func main() -> void {
        let small: [int; 2] = [1, 2];
        let large: [int; 4] = [1,2,3,4];
        
        large = small;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(IdLValue(large), Identifier(small))"

def test_080():
    """Test If else - Just If"""
    source = """   
    func main() -> void {
        let x = 1;
        if (x > 0) {
            x = 100;
        }
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_081():
    """Test If else - If else"""
    source = """   
    func main() -> void {
        let x = 1;
        if (x > 0) {
            x = 100;
        }
        else {
            x = 10;
        }
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_082():
    """Test If else - If else if else"""
    source = """   
    func main() -> void {
        let x = 1;
        if (x > 0) {
            x = 100;
        }
        else if (x == 0){
            let y = x;
        }
        else {
            x = 10;
        }
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_083():
    """Test func If else - If else if else missing return in elif"""
    source = """   
    func ifcond(x: int) -> string {
        if (x > 1) {
            return "Hello World";
        }
        else if (x == 0) {
            let y = x;
        }
        else {
            return "Hello";
        }
    }
    func main() -> void {
        let s = ifcond(3);
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: FuncDecl(ifcond, [Param(x, int)], string, [IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(1)), then_stmt=BlockStmt([ReturnStmt(StringLiteral('Hello World'))]), elif_branches=[(BinaryOp(Identifier(x), ==, IntegerLiteral(0)), BlockStmt([VarDecl(y, Identifier(x))]))], else_stmt=BlockStmt([ReturnStmt(StringLiteral('Hello'))]))])"

def test_084():
    """Test missing arg in func"""
    source = """   
    func returnVal() -> int {
        return x;
    }
    
    func main() -> void {
        let val = returnVal();
    }
    """
    assert Checker(source).check_from_source() == "Undeclared Identifier: x"

def test_085():
    """Test passing param in func - mising args"""
    source = """   
    func returnVal() -> int {
        return x;
    }
    
    func main() -> void {
        let val = returnVal(3);
    }
    """
    assert Checker(source).check_from_source() == "Undeclared Identifier: x"

def test_086():
    """Test initialize array without elements"""
    source = """  
    func main() -> void {
        let a: [float; 2] = [];
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: VarDecl(a, [float; 2], ArrayLiteral([]))"
    
def test_087():
    """Test Calling a identier as a func"""
    source = """  
    func main() -> void {
        let a = 5;
        let b = a();
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Expression: FunctionCall(Identifier(a), [])"

def test_088():
    """Test Pipeline"""
    source = """  
    func say() -> string {
        return "PPL";
    }
    
    func say1(s: string) -> string {
        return "Hi" + s;
    }
    
    func main() -> void {
        let a = say() >> say1();
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_089():
    """Test Break/continue in function scope"""
    source = """  
    func main() -> void {
        break;
    }
    """
    assert Checker(source).check_from_source() == "Must In Loop: BreakStmt()"

def test_090():
    """Test Break/continue in function scope"""
    source = """  
    func main() -> void {
        continue;
    }
    """
    assert Checker(source).check_from_source() == "Must In Loop: ContinueStmt()"

def test_091():
    """Test Break/continue in conditional blocks"""
    source = """  
    func main() -> void {
        if (true) {
            break;
        }
    }
    """
    assert Checker(source).check_from_source() == "Must In Loop: BreakStmt()"

def test_092():
    """Test Break/continue in conditional blocks"""
    source = """  
    func main() -> void {
        if (true) {
            continue;
        }
    }
    """
    assert Checker(source).check_from_source() == "Must In Loop: ContinueStmt()"

def test_093():
    """Test Break/continue in conditional blocks"""
    source = """  
    func main() -> void {
        if (true) {
            let x = 5;
        }
        else {
            break;
        }
    }
    """
    assert Checker(source).check_from_source() == "Must In Loop: BreakStmt()"

def test_094():
    """Test Break/continue in nested blocks"""
    source = """  
    func main() -> void {
        let x = 10;
        if (x > 2) {
            break;
        }
        else {
            continue;
        }
    }
    """
    assert Checker(source).check_from_source() == "Must In Loop: BreakStmt()"

def test_095():
    """Test Break/continue in while loops"""
    source = """  
    func main() -> void {
        let x = 10;
        while (x > 5) {
            if (x == 10) {
                break;
            }
            if (x % 2 == 0) {
                x = x + 1;
                continue;                  
            }
            x = x + 1;
        }
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_096():
    """Test Break/continue in while loops"""
    source = """  
    func main() -> void {
        let numbers = [1, 2, 3, 4, 5];
        for (num in numbers) {
            if (num == 3) {
                break;                       
            }
            if (num % 2 == 0) {
                continue;                  
            }
            let y = 1;
        }
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_097():
    """Test Break/continue in while loops"""
    source = """  
    func main() -> void {
        let i = 0;
        while (i < 5) {
            let j = 0;
            while (j < 5) {
                if (i == j) {
                    break;                   
                }
                if (j == 2) {
                    j = j + 1;
                    continue;
                }
                j = j + 1;
            }
            i = i + 1;
        }
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_098():
    """Test Break/continue after loop"""
    source = """
    func main() -> void {
        let i = 0;
        while (i < 5) {
            i = i + 1;
        }
        break;
    }
    """
    assert Checker(source).check_from_source() == "Must In Loop: BreakStmt()"

def test_099():
    """Test Break/continue in function called from loop"""
    source = """  
    func helperFunction() -> void {
        break;
        continue;
    }
    
    func main() -> void {
        helperFunction();
    }
    """
    assert Checker(source).check_from_source() == "Must In Loop: BreakStmt()"

def test_100():
    """Test program with no main function"""
    source = """
    func print(s: string) -> string {
        return s;
    } 
    
    func helper() -> void {
        print("Helper function");
    }
    
    func calculate(x: int) -> int {
        return x * 2;
    }
    """
    assert Checker(source).check_from_source() == "No Entry Point"

def test_101():
    """Test main function with wrong case-sensitive name"""
    source = """
    func print(s: string) -> string {
        return s;
    }
    
    func Main() -> void {
        print("Wrong case");
    }
    """
    assert Checker(source).check_from_source() == "No Entry Point"

def test_102():
    """Test main function with parameters"""
    source = """
    func print(s: string) -> string {
        return s;
    }
    
    func main(args: [string; 5]) -> void {
        print("With arguments");
    }
    """
    assert Checker(source).check_from_source() == "No Entry Point"

def test_103():
    """Test main function with non-void return type"""
    source = """
    func print(s: string) -> string {
        return s;
    }
    
    func main() -> int {
        print("Returns integer");
        return 0;
    }
    """
    assert Checker(source).check_from_source() == "No Entry Point"

def test_104():
    """Test multiple main functions"""
    source = """
    func print(s: string) -> string {
        return s;
    }
    
    func main() -> void {
        print("First main");
    }
    
    func main() -> void {
        print("Second main");
    }
    """
    assert Checker(source).check_from_source() == "Redeclared Function: main"

def test_105():
    """Test valid main function"""
    source = """
    func print(s: string) -> string {
        return s;
    }
    
    func main() -> void {
        print("Hello, World!");
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"

def test_106():
    """Test out-of-bounds array access in ArrayAccessLValue"""
    source = """
    func main() -> void {
        let numbers: [int; 5] = [1, 2, 3, 4, 5];
        numbers[10] = 0;
    }
    """
    assert Checker(source).check_from_source() == "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(numbers), IntegerLiteral(10)), IntegerLiteral(0))"

def test_107():
    """Test valid array operations"""
    source = """
    func main() -> void {
        let arr1: [int; 3] = [1, 2, 3];
        let arr2: [int; 3] = [4, 5, 6];
        arr1 = arr2;
        arr1[0] = 10;
        arr1[1] = arr2[2];
    }
    """
    assert Checker(source).check_from_source() == "Static checking passed"