from bangtal import *
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

scene_main = Scene('.', 'Images/scene_lunch.png')

class Digits: # currently, negative numbers cannot be processed.
    def __init__(self, number, x, y):
        self.objects_digit = self.make_objects(self.number_to_digits(number), x, y)
        self.x = x
        self.y = y
        self.show_objects(self.objects_digit)
    def number_to_digits(self, number):
        result = []
        while True:
            result.append(number%10)
            number //= 10
            if number == 0:
                break
        return result
    def make_objects(self, digits, x, y):
        result = []
        for i in range(len(digits)):
            object = Object('Images/'+str(digits[i])+'.png')
            object.locate(scene_main, x - i * 15, y) # 20
            result.append(object)
        return result
    def show_objects(self, objects):
        for i in objects:
            i.show()
    def reset_number(self, number):
        digits = self.number_to_digits(number)
        length = len(self.objects_digit)
        if length < len(digits):
            for i in range(length):
                self.objects_digit[i].setImage('Images/'+str(digits[i])+'.png')
            self.objects_digit.extend(self.make_objects(digits[length:], self.x-length*15, self.y)) # 20
        else:
            for i in range(length-len(digits)):
                self.objects_digit.pop().hide()
            for i in range(len(digits)):
                self.objects_digit[i].setImage('Images/'+str(digits[i])+'.png')
        self.show_objects(self.objects_digit)
widget_date = Object('Images/widget_date.png')
widget_date.locate(scene_main, 150, 620)
widget_date.show()
date = 6 # it must be synchronized with the day of the week information in one class.
widget_dayWeek = Object('Images/widget_saturday.png')
widget_dayWeek.locate(scene_main, 398, 620)
widget_dayWeek.show()
widget_dayTime = Object('Images/widget_lunch.png')
widget_dayTime.locate(scene_main, 480, 620)
widget_dayTime.show()
comeback = 0
limit = 21
def refresh_failed_and_final():
    global date, comeback, limit, night, failed, final
    
    date += comeback
    
    if date > limit-1:
        failed = True
    elif date == limit-1 and night:
        final = True
    
    if limit - date >= 0:
        date_digits.reset_number(limit - date)
def refresh_date():
    global date

    refresh_failed_and_final()
    
    date += 1
    date_digits.reset_number(limit - date)
date_digits = Digits(limit - date, 345, 636)

widget_stat = Object('Images/widget_stat.png')
widget_stat.locate(scene_main, 900, 175)
widget_stat.show()
fame = 50
fatigue = 30
health = 50
balance = 40
upperBody = 40
lowerBody = 50
AI = 30
fame_digits = Digits(fame, 1055, 634)
fatigue_digits = Digits(fatigue, 1055, 560)
health_digits = Digits(health, 1055, 486)
balance_digits = Digits(balance, 1055, 412)
upperBody_digits = Digits(upperBody, 1055, 340)
lowerBody_digits = Digits(lowerBody, 1055, 265)
AI_digits = Digits(AI, 1055, 190)

class Menu(Object):
    def __init__(self, image):
        super().__init__(image)
        self.children = []
        self.clicked = False
        self.leaf = True
        self.height = 0
    def add_child(self, child):
        self.leaf = False
        self.children.append(child)
        child.refresh_height(self.height)
    def change_child(self, index, child):
        target = self.children[index-1]
        target.hide_children(target.height)
        target.hide()
        self.children[index-1] = child
        child.refresh_height(self.height)
    def refresh_height(self, height):
        self.height = height + 1
        for i in self.children:
            i.refresh_height(self.height)
    def hide_children(self, height):
        if self.height > height:
            self.hide()
            self.clicked = False
        for i in self.children:
            i.hide_children(height)
    def onMouseAction(self, x, y, action):
        if self.clicked:
            self.hide_children(self.height)
            self.clicked = False
        else:
            for i in self.children:
                i.show()
            self.clicked = True

class RootMenu(Menu):
    def __init__(self, image, roots):
        super().__init__(image)
        self.roots = roots
        roots.append(self)
    def onMouseAction(self, x, y, action):
        super().onMouseAction(x, y, action)
        for i in self.roots:
            if i is not self:
                i.hide_children(i.height)
                i.clicked = False
        
roots = []
text = ''

button_go_menu = RootMenu('Images/button_go_menu.png', roots)
button_go_menu.locate(scene_main, 900, 105)
button_go_menu.show()
button_menu_save = Menu('Images/button_menu_save.png')
button_menu_save.locate(scene_main, 150, 175)
button_go_menu.add_child(button_menu_save)
def save_file(x,y,action):
    showMessage('미구현')
button_menu_save.onMouseAction = save_file
button_menu_load = Menu('Images/button_menu_load.png')
button_menu_load.locate(scene_main, 150, 105)
button_go_menu.add_child(button_menu_load)
def load_file(x,y,action):
    showMessage('미구현')
button_menu_load.onMouseAction = load_file
button_menu_exit = Menu('Images/button_game_exit.png')
button_menu_exit.locate(scene_main, 150, 35)
button_go_menu.add_child(button_menu_exit)
def exit_game(x,y,action):
    endGame()
button_menu_exit.onMouseAction = exit_game

import random
count_click = 0
base_penalty = 0
scene_train = Scene('.', 'Images/scene_train.png')
button_up_stat = Object('Images/button_up_stat.png')
button_up_stat.locate(scene_train, 900, 210)
button_up_stat.show()
def up_balance(x,y,action):
    global fatigue, health, balance, count_click, base_penalty
    result_fatigue = fatigue + 5 + count_click + base_penalty
    result_balance = balance + 1
    if result_fatigue > health:
        showMessage("활력이 모자랍니다.")
    else:
        fatigue = result_fatigue
        balance = result_balance
        fatigue_digits.reset_number(fatigue)
        balance_digits.reset_number(balance)
        count_click += 1
        showMessage('피로 '+str(fatigue)+' 체력 '+str(health)+' 균형 '+str(balance))
def up_upperBody(x,y,action):
    global fatigue, health, upperBody, count_click, base_penalty
    result_fatigue = fatigue + 7 + count_click + base_penalty
    result_health = health + 1
    result_upperBody = upperBody + 1
    if result_fatigue > health:
        showMessage("활력이 모자랍니다.")
    else:
        fatigue = result_fatigue
        health = result_health
        upperBody = result_upperBody
        fatigue_digits.reset_number(fatigue)        
        health_digits.reset_number(health)
        upperBody_digits.reset_number(upperBody)
        count_click += 1
        showMessage('피로 '+str(fatigue)+' 체력 '+str(health)+' 상체 '+str(upperBody))
def up_lowerBody(x,y,action):
    global fatigue, health, lowerBody, count_click, base_penalty
    result_fatigue = fatigue + 10 + count_click + base_penalty
    result_health = health + 1
    result_lowerBody = lowerBody + 1
    if result_fatigue > health:
        showMessage("활력이 모자랍니다.")
    else:
        fatigue = result_fatigue
        health = result_health
        lowerBody = result_lowerBody
        fatigue_digits.reset_number(fatigue)
        health_digits.reset_number(health)
        lowerBody_digits.reset_number(lowerBody)
        count_click += 1
        showMessage('피로 '+str(fatigue)+' 체력 '+str(health)+' 하체 '+str(lowerBody))
button_down_stat = Object('Images/button_down_stat.png')
button_down_stat.locate(scene_train, 1021, 210)
button_down_stat.show()
def down_balance(x,y,action):
    global fatigue, health, balance, count_click, base_penalty
    if count_click == 0:
        showMessage("할당한 운동 횟수가 없습니다.")
    else:
        count_click -= 1
        fatigue -= (5 + count_click + base_penalty) 
        balance -= 1
        fatigue_digits.reset_number(fatigue)
        balance_digits.reset_number(balance)
        showMessage('피로 '+str(fatigue)+' 체력 '+str(health)+' 균형 '+str(balance))
def down_upperBody(x,y,action):
    global fatigue, health, upperBody, count_click, base_penalty
    if count_click == 0:
        showMessage("할당한 운동 횟수가 없습니다.")
    else:
        count_click -= 1
        fatigue -= (7 + count_click + base_penalty) 
        health -= 1
        upperBody -= 1
        fatigue_digits.reset_number(fatigue)
        health_digits.reset_number(health)
        upperBody_digits.reset_number(upperBody)
        showMessage('피로 '+str(fatigue)+' 체력 '+str(health)+' 상체 '+str(upperBody))
def down_lowerBody(x,y,action):
    global fatigue, health, lowerBody, count_click, base_penalty
    if count_click == 0:
        showMessage("할당한 운동 횟수가 없습니다.")
    else:
        count_click -= 1
        fatigue -= (10 + count_click + base_penalty) 
        health -= 1
        lowerBody -= 1
        fatigue_digits.reset_number(fatigue)
        health_digits.reset_number(health)
        lowerBody_digits.reset_number(lowerBody)
        showMessage('피로 '+str(fatigue)+' 체력 '+str(health)+' 하체 '+str(lowerBody))
button_exit_train = Object('Images/button_menu_exit.png')
button_exit_train.locate(scene_train, 900, 140)
button_exit_train.show()
def exit_train(x,y,action):
    global count_click
    if count_click == 0:
        scene_main.enter()
    else:
        refresh_game()
        scene_main.enter()
button_exit_train.onMouseAction = exit_train

button_go_schedule = RootMenu('Images/button_go_schedule.png', roots)
button_go_schedule.locate(scene_main, 900, 35)
button_go_schedule.show()

button_schedule_train = Menu('Images/button_schedule_train.png')
button_schedule_train.locate(scene_main, 150, 175)
button_schedule_train_balance = Menu('Images/button_schedule_train_balance.png')
button_schedule_train_balance.locate(scene_main, 150, 315)
button_schedule_train.add_child(button_schedule_train_balance)
def train_balance(x,y,action):
    global count_click, base_penalty
    count_click = 0
    base_penalty = fatigue // 10
    button_up_stat.onMouseAction = up_balance
    button_down_stat.onMouseAction = down_balance
    scene_train.enter()
button_schedule_train_balance.onMouseAction = train_balance
button_schedule_train_upperBody = Menu('Images/button_schedule_train_upperBody.png')
button_schedule_train_upperBody.locate(scene_main, 150, 245)
button_schedule_train.add_child(button_schedule_train_upperBody)
def train_upperBody(x,y,action):
    global count_click, base_penalty
    count_click = 0
    base_penalty = fatigue // 10
    button_up_stat.onMouseAction = up_upperBody
    button_down_stat.onMouseAction = down_upperBody
    scene_train.enter()
button_schedule_train_upperBody.onMouseAction = train_upperBody
button_schedule_train_lowerBody = Menu('Images/button_schedule_train_lowerBody.png')
button_schedule_train_lowerBody.locate(scene_main, 150, 175)
button_schedule_train.add_child(button_schedule_train_lowerBody)
def train_lowerBody(x,y,action):
    global count_click, base_penalty
    count_click = 0
    base_penalty = fatigue // 10
    button_up_stat.onMouseAction = up_lowerBody
    button_down_stat.onMouseAction = down_lowerBody
    scene_train.enter()
button_schedule_train_lowerBody.onMouseAction = train_lowerBody

button_schedule_promotion = Menu('Images/button_schedule_promotion.png')
button_schedule_promotion.locate(scene_main, 150, 175)
def club_promotion(x,y,action):
    global fame, fatigue, health, text
    if health >= fatigue + 5:
        result = random.randrange(3)
        fame += result
        fatigue += 5
        fame_digits.reset_number(fame)
        fatigue_digits.reset_number(fatigue)
        text = '구단 행사 완료! 명성 '+str(result)+' 피로 5'
        refresh_game()
    else:
        showMessage('활력이 부족합니다.')
button_schedule_promotion.onMouseAction = club_promotion

scene_stadium = Scene('.', 'Images/scene_stadium.png')
button_schedule_match = Menu('Images/button_schedule_match.png')
button_schedule_match.locate(scene_main, 150, 35)
vigor = 0
def match_and_interview(x,y,action):
    global fame, fatigue, health, balance, upperBody, lowerBody, AI, vigor, comeback, text
    scene_stadium.setImage('Images/scene_stadium.png')
    scene_stadium.enter()
    case = 1
    if health == fatigue:
        vigor = 0
    else:
        vigor = random.randrange(int((health+1 - fatigue)*2/3),(health+1 - fatigue))
    log_fatigue = fatigue
    fatigue += vigor
    log_health = health
    log_balance = balance
    log_upperBody = upperBody
    log_lowerBody = lowerBody
    log_AI = AI
    
    projector = Timer(1)
    def play_scenes(self, case):
        global fame, fatigue, health, balance, upperBody, lowerBody, AI, vigor, offensive_point, comeback, text
        print(vigor)
        time = 2
        if case == 0:
            scene_stadium.setImage('Images/scene_finished.png')
            showMessage('손흥민의 활약은 여기까지 입니다. 경기 종료.')
            case = 6
        elif case == 1:
            showMessage('경기를 시작합니다.') # starting list
            offensive_point = 0
            case = 2
        elif case == 2:
            chance = random.randrange(1, 101)
            if chance <= 45 and random.randrange(1, 101) <= vigor/3 + lowerBody/3 + AI/3:
                scene_stadium.setImage('Images/scene_chance.png')
                showMessage('손흥민이 골키퍼 근처에서 공을 잡고 있습니다.')
                case = 3
                vigor -= 2
                health += 1
            elif chance > 55 and random.randrange(1, 101) <= vigor/3 + lowerBody/3 + AI/3:
                scene_stadium.setImage('Images/scene_chance.png')
                showMessage('손흥민이 골키퍼 멀리서 공을 잡고 있습니다.')
                case = 4
                vigor -= 1.5
                health += 1
            else:
                scene_stadium.setImage('Images/scene_patrol.png')
                showMessage('손흥민이 기회를 노리고 있습니다.')
                time = 0.5
                vigor -= 1
                if vigor > 0:
                    case = 2
                else:
                    case = 0
        elif case == 3:
            scene_stadium.setImage('Images/scene_shooting.png')
            if random.randrange(1, 101) <= balance/3 + upperBody/6 + lowerBody/3 + AI/6:
                showMessage('슛~ 손흥민이 공격 포인트를 추가해냅니다!.')
                offensive_point += 1
            else:
                showMessage('슛~ 하지만 공격 포인트를 추가해내지 못합니다.')
            vigor -= 0.5
            if vigor <= 0:
                case = 0
            else:
                case = 2
        elif case == 4:
            scene_stadium.setImage('Images/scene_shooting.png')
            chance = random.randrange(1, 101)
            if chance <= 10:
                if random.randrange(1, 101) <= balance/3 + lowerBody/3:
                    showMessage('중거리 슛~ 손흥민이 공격 포인트를 추가해냅니다!.')
                    offensive_point += 1
                else:
                    showMessage('중거리 슛~ 하지만 공격 포인트를 추가해내지 못합니다.')
                vigor -= 1
                if vigor <= 0:
                    case = 0
                else:
                    case = 2
            else:
                if random.randrange(1, 101) <= vigor/5 + balance/5 + upperBody/5 + lowerBody/5 + AI/5:
                    scene_stadium.setImage('Images/scene_outpace.png')
                    showMessage('손흥민이 수비 라인을 제쳐냅니다.')
                    vigor -= 3
                    balance += 1
                    upperBody += 1
                    lowerBody += 1
                    AI += 1
                    case = 3
                else:
                    scene_stadium.setImage('Images/scene_lose_ball.png')
                    showMessage('손흥민이 수비 라인을 제쳐내지 못합니다.')
                    vigor -= 2.5
                    if random.randrange(0, 100) < 10:
                        comeback = random.randrange(7)
                        case = 5
                    elif vigor <= 0:
                        case = 0
                    else:
                        case = 2
        elif case == 5:
            scene_stadium.setImage('Images/scene_injury.png')
            showMessage('손흥민이 부상당했습니다! 복귀까지 수일이 걸릴 것으로 예상됩니다.')
            refresh_failed_and_final()
            case = 6
        else:
            scene_main.enter()
            if vigor <= 0:
                health += vigor
            health = int(health)
            fame += offensive_point
            text = ('공격포인트 및 명성 '+str(offensive_point)
                        +' 피로 '+str(fatigue-log_fatigue)
                        +' 체력 '+str(health-log_health)
                        +' 균형 '+str(balance-log_balance)
                        +' 상체 '+str(upperBody-log_upperBody)
                        +' 하체 '+str(lowerBody-log_lowerBody)
                        +' 판단 '+str(AI-log_AI)
                        +' 재활 소요 일수 '+str(comeback))
            fame_digits.reset_number(fame)
            fatigue_digits.reset_number(fatigue)
            health_digits.reset_number(health)
            balance_digits.reset_number(balance)
            upperBody_digits.reset_number(upperBody)
            lowerBody_digits.reset_number(lowerBody)
            AI_digits.reset_number(AI)
            refresh_game()
            comeback = 0
            return
                      
        self.set(time)
        self.onTimeout = lambda : play_scenes(projector, case)
        self.start()
    projector.onTimeout = lambda : play_scenes(projector, case)
    projector.start()
button_schedule_match.onMouseAction = match_and_interview
button_go_schedule.add_child(button_schedule_match)

button_schedule_relax = Menu('Images/button_schedule_relax.png')
button_schedule_relax.locate(scene_main, 150, 105)
def rest_or_outgo(x,y,action):
    global fatigue, text
    if fatigue > 0:
        result = random.randrange(int(min(20, fatigue)/4), min(20, fatigue) + 1)
    else:
        result = 0
    fatigue -= result
    fatigue_digits.reset_number(fatigue)
    text = '피로 회복 완료! 피로 -'+str(result)
    refresh_game()
button_schedule_relax.onMouseAction = rest_or_outgo

button_schedule_AI = Menu('Images/button_schedule_AI.png')
button_schedule_AI.locate(scene_main, 150, 35)
def study_AI(x,y,action):
    global fatigue, health, AI, text
    if health >= fatigue + 5:
        result = random.randrange(3)
        fatigue += 5
        AI += result
        fatigue_digits.reset_number(fatigue)
        AI_digits.reset_number(AI)
        text = '전술 훈련 완료! 피로 5 판단 '+str(result)
        refresh_game()
    else:
        showMessage('활력이 부족합니다.')
button_schedule_AI.onMouseAction = study_AI

button_schedule_interview = Menu('Images/button_schedule_interview.png')
button_schedule_interview.locate(scene_main, 150, 35)
def get_analysis(x,y,action):
    global fatigue, health, balance, AI, text
    if health >= fatigue + 5:
        fatigue += 5
        result_balance = random.randrange(-1, 3)
        result_AI = random.randrange(-1, 3)
        balance += result_balance
        AI += result_AI
        fatigue_digits.reset_number(fatigue)
        balance_digits.reset_number(balance)
        AI_digits.reset_number(AI)
        text = '선수 코칭 완료! 피로 5 균형 '+str(result_balance)+' 판단 '+str(result_AI)
        refresh_game()
    else:
        showMessage('활력이 부족합니다.')
button_schedule_interview.onMouseAction = get_analysis

scene_OXquiz = Scene('.', 'Images/scene_quiz.png')
button_o = Object('Images/o.png')
button_o.locate(scene_OXquiz, 325, 150)
def button_o_mouse_action(x, y, action):
    global quiz_index, passed
    if quiz_index == 0:
        showMessage("정답입니다.")
        passed = True
    elif quiz_index == 1:
        showMessage("오답입니다. 공을 받을 선수 앞에 상대 선수가 2명 미만으로 있을 때여야 합니다.")
        passed = False
    '''
    elif quiz_index == 2:
        showMessage("오답입니다. 초대 월드컵 우승팀은 우루과이입니다.")
        passed = False
    elif quiz_index == 3:
        showMessage("정답입니다. 클로제는 월드컵 통산 16골을 기록했습니다.")
        passed = True
    elif quiz_index == 4:
        showMessage("정답입니다. 총 20회 우승했습니다.")
        passed = True
    elif quiz_index == 5:
        showMessage("정답입니다. 1954년 스위스월드컵에서 대한민국은 헝가리에게 9:0으로 패배했습니다.")
        passed = True
    '''
    quiz_timer.stop()
    button_exit_quiz.show()
    button_o.hide()
    button_x.hide()
button_o.onMouseAction = button_o_mouse_action
button_x = Object('Images/x.png')
button_x.locate(scene_OXquiz, 645, 150)
def button_x_mouse_action(x, y, action):
    global quiz_index, passed
    if quiz_index == 0:
        showMessage("오답입니다. 공격 측 선수였다면 성공할 경우 다시, 수비 측 선수였다면 실패할 경우 다시 찹니다.")
        passed = False
    elif quiz_index == 1:
        showMessage("정답입니다.")
        passed = True
    '''
    elif quiz_index == 2:
        showMessage("정답입니다.")
        passed = True
    elif quiz_index == 3:
        showMessage("오답입니다. 클로제는 월드컵 통산 16골로 역대 1위가 맞습니다.")
        passed = False
    elif quiz_index == 4:
        showMessage("오답입니다. 맨체스터 유나이티드는 20회 우승으로, 최다 우승팀입니다.")
        passed = False
    elif quiz_index == 5:
        showMessage("오답입니다. 1954년 스위스월드컵에서 대한민국은 헝가리에게 9:0으로 패배했습니다.")
        passed = False
    '''
    quiz_timer.stop()
    button_exit_quiz.show()
    button_o.hide()
    button_x.hide()
button_x.onMouseAction = button_x_mouse_action
quiz_index = 0
passed = False
question = ['페널티킥을 찰 때 키커가 차기 전에 다른 선수가 페널티 박스 안으로 들어오면 페널티 킥이 다시 주어진다.',
            '공을 가진 선수가 상대 진영에 있는, 공보다 앞에 있는 자기편 선수에게 패스하면 오프사이드 반칙이다.',
            '초대 월드컵 우승팀은 브라질이다.', 
            '월드컵 통산 최다골 기록을 보유한 선수는 독일의 클로제이다.',
           '잉글랜드 프리미어리그 역대 최다 우승팀은 맨체스터 유나이티드이다.'
           '대한민국은 월드컵 역대 최다 득점차 패배의 기록을 가지고 있다.']
#answer = ['o', 'x']
quiz_timer = Timer(5)
def quiz_result():
    global passed
    showMessage('시간초과!')
    passed = False
    button_o.hide()
    button_x.hide()
    button_exit_quiz.show()
quiz_timer.onTimeout = quiz_result
button_exit_quiz = Object('Images/button_menu_exit.png')
button_exit_quiz.locate(scene_OXquiz, 900, 35)
def exit_quiz(x,y,action):
    global passed, AI, quiz_index, text

    result_AI = 0

    if passed:
        result_AI = 5

    AI += result_AI
    AI_digits.reset_number(AI)
    quiz_index += 1
    scene_main.enter()
    text = 'OX 퀴즈 결과 : 피로 5 판단 '+str(result_AI)
    refresh_game()
button_exit_quiz.onMouseAction = exit_quiz
button_schedule_quiz = Menu('Images/button_schedule_quiz.png')
button_schedule_quiz.locate(scene_main, 150, 35)
def OX_quiz(x,y,action):
    global fatigue, health, quiz_index
    if health >= fatigue + 0:
        fatigue += 0
        fatigue_digits.reset_number(fatigue)
        scene_OXquiz.enter()
        button_o.show()
        button_x.show()
        showMessage(question[quiz_index])
        quiz_timer.set(5)
        quiz_timer.start()
    else:
        showMessage('활력이 부족합니다.')
button_schedule_quiz.onMouseAction = OX_quiz

scene_roulette = Scene(".","images/scene_roulette.png")
pick = Object("images/button_pick.png")
pick.setScale(0.35)
pick.locate(scene_roulette, 1100, 30)
pick.show()
end = Object("images/button_end.png")
end.locate(scene_roulette, 1050, 600)
def end_onMouseAction(x, y, action):
    pick.show()
    item.hide()
    end.hide()
    scene_main.enter()
    refresh_game()
end.onMouseAction = end_onMouseAction
item = Object("images/보호대.png")
item.locate(scene_roulette, 550, 250)

pressed = False
case = 0
roulette = Timer(0.05)
def pick_onMouseAction(x,y, action): # if you do it 3 times in a row it is a slot machine.
    global pressed, case, health, balance, upperBody, lowerBody, AI, comeback, text
    if pressed:
        roulette.stop()
        roulette.set(0.05)
        pick.hide()
        end.show()

        health+=5
        balance+=5
        upperBody+=5
        lowerBody+=5
        AI+=5

        if case == 0:
            lowerBody += 5
            item.setImage("images/보호대.png")
            showMessage("정강이 보호대를 획득했습니다. 하체 추가 +5")
        elif case == 1:
            upperBody += 5
            item.setImage("images/유니폼상의.png")
            showMessage("유니폼 상의를 획득했습니다. 상체 추가 +5")
        elif case == 2:
            balance += 5
            item.setImage("images/유니폼하의.png")
            showMessage("유니폼 하의를 획득했습니다. 균형 추가 +5")
        elif case == 3:
            AI += 5
            item.setImage("images/축구공.png")
            showMessage("축구공을 획득했습니다. 판단 추가 +5")
        else:
            health += 5
            item.setImage("images/축구양말.png")
            showMessage("축구양말을 획득했습니다. 체력 추가 +5")
        text = '육성 부스터 사용 완료. 5일 동안 모든 스탯 +5'
        
        health_digits.reset_number(health)
        balance_digits.reset_number(balance)
        upperBody_digits.reset_number(upperBody)
        lowerBody_digits.reset_number(lowerBody)
        AI_digits.reset_number(AI)
        comeback = 5
        refresh_failed_and_final()
        comeback = 0
        pressed = False
    else:
        item.show()
        def play_objects(self):
            global case
            if case == 0:
                item.setImage("images/보호대.png")
            elif case == 1:
                item.setImage("images/유니폼상의.png")
            elif case == 2:
                item.setImage("images/유니폼하의.png")
            elif case == 3:
                item.setImage("images/축구공.png")
            elif case == 4:
                item.setImage("images/축구양말.png")
            case = (case + 1)%5
            self.set(0.05)
            self.onTimeout = lambda : play_objects(self)
            self.start()
        roulette.onTimeout = lambda : play_objects(roulette)
        roulette.start()
        pressed = True
pick.onMouseAction = pick_onMouseAction

button_schedule_buff = Menu('Images/button_schedule_buff.png')
button_schedule_buff.locate(scene_main, 150, 35)
def buff_debuff(x,y,action):
    global fatigue, health
    if health >= fatigue + 0:
        fatigue += 0
        fatigue_digits.reset_number(fatigue)
        scene_roulette.enter()
        showMessage("우측 하단 뽑기 버튼을 눌러주세요!")
    else:
        showMessage('활력이 부족합니다.')
button_schedule_buff.onMouseAction = buff_debuff

scene_report = Scene('.', 'Images/scene_report.png')
button_exit_report = Object('Images/button_menu_exit.png')
button_exit_report.locate(scene_report, 900, 35)
button_exit_report.show()
def exit_report(x,y,action):
    endGame()
button_exit_report.onMouseAction = exit_report

failed = False
final = False
night = False
def refresh_game():
    global date, comeback, night, failed, final, fatigue, text, roots
    day_of_week = (date - 1) % 7 + 1

    for i in roots:
        i.hide_children(i.height)
        i.clicked = False

    if failed:
        scene_report.enter()
        text+='. 손흥민은 부상으로 시즌을 마감했습니다.'
    elif final:
        print(fame)
        def final_report(x,y,action):
            scene_report.setImage('Images/scene_final.png')
            showMessage('이용해주셔서 감사합니다.')
            button_exit_report.onMouseAction = exit_report
        button_exit_report.onMouseAction = final_report
        if fame >= 60:
            scene_report.setImage('Images/scene_tryout.png')
            scene_report.enter()
            text+='. 손흥민은 토트넘에 입단했습니다.'
        else:
            scene_report.setImage('Images/scene_remain.png')
            scene_report.enter()
            text+='. 손흥민은 잔류하기로 했습니다.'
    elif night:
        if fatigue > 0:
            result = random.randrange(int(min(30, fatigue)/5), min(30, fatigue) + 1)
        else:
            result = 0
        fatigue -= result
        fatigue_digits.reset_number(fatigue)
        if text is '':
            text = '취침 후 아침 훈련 마친 현재까지 추가 피로 -'+str(result)
        else:
            text+='. 취침 후 아침 훈련 마친 현재까지 추가 피로 -'+str(result)
            
        refresh_date()
        if final:
            refresh_game()
        else:
            scene_main.setImage('Images/scene_lunch.png')
            widget_dayTime.setImage('Images/widget_lunch.png')
            button_go_schedule.change_child(3, button_schedule_AI)
            if day_of_week == 7:
                widget_dayWeek.setImage('Images/widget_monday.png')
                button_go_schedule.change_child(1, button_schedule_train)
            elif day_of_week == 1:
                widget_dayWeek.setImage('Images/widget_tuesday.png')
                button_go_schedule.change_child(1, button_schedule_train)
            elif day_of_week == 2:
                widget_dayWeek.setImage('Images/widget_wednesday.png')
                button_go_schedule.change_child(1, button_schedule_promotion)
            elif day_of_week == 3:
                widget_dayWeek.setImage('Images/widget_thursday.png')
                button_go_schedule.change_child(1, button_schedule_train)
            elif day_of_week == 4:
                widget_dayWeek.setImage('Images/widget_friday.png')
                button_go_schedule.change_child(1, button_schedule_train)
            elif day_of_week == 5:
                widget_dayWeek.setImage('Images/widget_saturday.png')
                button_go_schedule.children = []
                button_go_schedule.add_child(button_schedule_match)
            else:
                widget_dayWeek.setImage('Images/widget_sunday.png')
                button_go_schedule.change_child(1, button_schedule_train)
                button_go_schedule.change_child(3, button_schedule_quiz)
            night = False
    else:
        scene_main.setImage('Images/scene_night.png')
        widget_dayTime.setImage('Images/widget_night.png')
        
        if day_of_week == 6 or comeback > 0 and day_of_week != 7:
            button_go_schedule.children = []
            button_go_schedule.add_child(button_schedule_train)
            button_go_schedule.add_child(button_schedule_relax)
            button_go_schedule.add_child(button_schedule_interview)
        elif day_of_week == 7 and comeback == 0:
            button_go_schedule.change_child(3, button_schedule_buff)
        elif day_of_week == 7 and comeback > 0:
            button_go_schedule.children = []
            button_go_schedule.add_child(button_schedule_train)
            button_go_schedule.add_child(button_schedule_relax)
            button_go_schedule.add_child(button_schedule_buff)
        elif day_of_week == 3:
            button_go_schedule.change_child(1, button_schedule_train)
            button_go_schedule.change_child(3, button_schedule_interview)
        else:
            button_go_schedule.change_child(3, button_schedule_interview)

        if day_of_week == 1:
            widget_dayWeek.setImage('Images/widget_monday.png')
        elif day_of_week == 2:
            widget_dayWeek.setImage('Images/widget_tuesday.png')
        elif day_of_week == 3:
            widget_dayWeek.setImage('Images/widget_wednesday.png')
        elif day_of_week == 4:
            widget_dayWeek.setImage('Images/widget_thursday.png')
        elif day_of_week == 5:
            widget_dayWeek.setImage('Images/widget_friday.png')
        elif day_of_week == 6:
            widget_dayWeek.setImage('Images/widget_saturday.png')
        else:
            widget_dayWeek.setImage('Images/widget_sunday.png')

        night = True
        
    if text is not '':
        showMessage(text)    
        text = ''

scene_intro = Scene('.', 'Images/scene_intro.png')
showMessage('손흥민 키우기 이지 모드')
skip_timer = Timer(2)
def enter_main():
    scene_main.enter()
    showMessage('* 과제 제출용으로 게임을 제작하기 위해 손흥민 선수의 사진을 사용했습니다. 저작권자 분들께 양해를 부탁드립니다.')
skip_timer.onTimeout = enter_main
skip_timer.start()
startGame(scene_intro)
