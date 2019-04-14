from sys import argv #"sys" 꾸러미에서 실행인자 값을 받는 "argv"를 가져다 쓴다.

#[1]스크립트에 전달할 실행 인자들을 나열한다.
스크립트, 파일_이름 = argv

#[2]open함수를 호출하여 파일을 열고 그 내용을 "텍스트" 변수에 저장한다.
#print("파일 이름을 입력해 주세요.")
#파일_이름 = input("]# ")
텍스트 = open(파일_이름, encoding='utf-8')

#[3]"파일 ex15_sample.txt의 내용:"이라고 화면에 출력한다.
print(f"파일 {파일_이름}의 내용:")

#[4]텍스트 변수에 저장된 내용을 read 함수로 읽어들여 화면에 출력한다.
print(텍스트.read())

#[5]"파일 이름을 다시 입력해 주세요"를 화면에 출력한다.
print("파일 이름을 다시 입력해 주세요.")
#[6]input 함수에 ">"을 미리 넣어두고 "파일_한번더" 변수에 저장한다.
파일_한번더 = input(">")

#[7]"파일_한번더"에 저장된 변수 ">"를 출력하고, 사용자의 입력을 기다린다.
#[8]사용자가 입력하면 이를 "텍스트_한번더" 변수에 저장한다.
텍스트_한번더 = open(파일_한번더, encoding='utf-8')

#[9]"텍스트_한번더"에 저장된 내용을 read 함수로 읽어서 화면에 출력한다.
print(텍스트_한번더.read())
