import traceback
import re


class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1


def match(string, pattern):
    if re.match(r'[^da* ]', pattern):
        raise ValueError('Invalid characters in pattern')
    
    if len(string) == len(pattern):
        for i in range(len(string)):
            if ((pattern[i]=='d' and re.match(r'[^\d]', string[i])) or (pattern[i]=='a' and re.match(r'[^a-z]', string[i]))
                or (pattern[i]=='*' and re.match(r'[^0-9a-z]', string[i])) or (pattern[i]==' ' and re.match(r'[^ ]', string[i]))):
                return False
    else:
        return False
    
    return True

             
def testMatch():
    runner = TestRunner('match')

    
    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ',  'a'))

    runner.expectTrue(lambda:  match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda:  match('x', 'w'))



tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}


def findGroup(tasks, groupId):
    if tasks['id'] == groupId:
        return tasks
    else:
        if 'children' in tasks:
            for task_child in tasks['children']:
                group = findGroup(task_child, groupId)
                if group:
                    return group


def findTaskHavingMaxPriority(group, current_max_priority, current_task_having_max_priority):
    max_priority = current_max_priority
    task_having_max_priority = current_task_having_max_priority
    
    for task_child in group['children']:
        if 'priority' in task_child:
            if max_priority == None or max_priority < task_child['priority']:
                max_priority = task_child['priority']
                task_having_max_priority = task_child
        else:
            task = findTaskHavingMaxPriority(task_child, max_priority, task_having_max_priority)
            if task:
                max_priority = task['priority']
                task_having_max_priority = task
            
    return task_having_max_priority


def findTaskHavingMaxPriorityInGroup(tasks, groupId):
    desired_group = findGroup(tasks, groupId)
    
    if desired_group == None:
        raise('Group not exist')
    elif 'priority' in desired_group:
        raise('Not a group')
    else:
        return findTaskHavingMaxPriority(desired_group, None, None)



def taskEquals(a, b):
    return (
        not 'children' in a and
        not 'children' in b and
        a['id'] == b['id'] and
        a['name'] == b['name'] and
        a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)

testMatch()
testFindTaskHavingMaxPriorityInGroup()
