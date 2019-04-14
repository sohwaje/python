# argv를 쓴 스크립트와 비슷한 함수 만들기
#[1]함수를 정의(def, define)한다.
#함수의 이름은 짧아야 한다.
#"*args"는  arguments의 약자이다.
#전달인자를 받는 argv와 비슷하게 작동한다. 소괄호 안에 써야 한다. ":"를 붙인다.
#함수를 정의했으면 다음 줄부터는 이 함수에 속하는 것임을 알리기 위해 반드시 들여쓰기를 한다.
#들여쓴 줄의 첫 줄은 실행인자를 풀어 놓는 unpack 코드이다.
def 둘_출력(*args):  #함수 정의
    실행인자1, 실행인자2 = args  #unpack 코드
    print(f"실행인자1: {실행인자1}, 실행인자2: {실행인자2}")


#[2]사실 args는 필요없다. unpack코드 없이 함수와 실행인자를 함께 쓸 수 있다.
def 둘_출력_다르게(실행인자1, 실행인자2):
    print(f"실행인자1: {실행인자1}, 실행인자2: {실행인자2}")

#[3]이 함수는 실행인자를 1개만 받는다.
def 하나_출력(실행인자1):
    print(f"실행인자1: {실행인자1}")

#[4]이 함수는 실행인자를 받지 않는다.
def 영_출력():
    print("아무것도 받지 않음")

#연습
def _yusung_(string1, string2):
    print(f"string1: {string1}, string2: {string2}")


#[5]함수의 실행인자들
둘_출력('유성', '이')
둘_출력_다르게('유성', '이')
하나_출력('하나!')
영_출력()
_yusung_('yusung', 'Lee')
