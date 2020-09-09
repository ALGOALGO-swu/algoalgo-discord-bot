from collections import Counter

# 가게에서 팔 아이템들 showuserinfo에서 나오는 item값들을 표현하는데 필요
shop={"STEP", "REDEMPTION", "SNAKE", "ASSASSIN", "STUN", "CAFFEINE", "REDBULL", "BOMB"}
# 유저들이 갖고있는 아이템 목록(db에서 가져올 예정): shop봇에서 아이템명+";"과 같이 저장되므로 따왔다.
# sql = "select items from member where discord_id='{str(author)}'"
item = "STEP;STEP;SNAKE;BOMB;ASSASSIN;STEP;"
itemlist=item.split(";")
count = Counter(itemlist)

# showuserinfo? 에서 나오는 item값은 갯수표현x 
# 따라서 set으로 그냥 있는거만 보여줘도 될듯
# print(shop&itemlist)
itemlists = list(shop&set(itemlist))
# 인덱스 및 아이템 갯수 넣기
# step = count["step"]
index = len(count)-1
for id,it in zip(range(index),itemlists):
    print(id+1,".",it,":",count[it],"개")

# ====================================================================
# 해야할 것 (데이터베이스 구현 참고)
# 인덱스 번호와 아이템명으로 입력받아 아이템 사용하게 하기
# 아이템의 유무 확인 검사 
# 걱정되는 것: 이미 함수 실행 중인데 다시 input값을 받아 사용할 수 있는가? 
# https://blog.yonghyeon.com/9 해당 블로그 참고: 사용자에게 다시 입력받기 활용 예제 - 가위바위보
# 입력받는 시간 5초 대기
# [*]:조회, [!]:에러, [+]:db에 추가/수정,[-]: db에 삭제,[INFO]:로그에 추가 알림사항
# 언어는 영어로
# ====================================================================









