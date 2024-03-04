class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.average_grade = []

    def rate_lec(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and course in self.courses_in_progress
                and course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __grade_total(self):
        for course in self.courses_in_progress:
            self.average_grade.append(sum(self.grades[course])/len(
                self.grades[course]))
        for fin_course in self.finished_courses:
            self.average_grade.append(sum(self.grades[fin_course])/len(
                self.grades[fin_course]))
        return round(sum(self.average_grade)/len(self.average_grade), 1) if len(
            self.average_grade) > 0 else 0

    def __str__(self):
        return (f'Имя: {self.name}\nФамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {self.__grade_total()}\n'
                f'Курсы в процессе изучения: '
                f'{", ".join(self.courses_in_progress)}\n'
                f'Завершенные курсы: {", ".join(self.finished_courses)}')

    def __lt__(self, other):
        return self.__grade_total() < other.__grade_total()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.average_grade = []

    def __grade_total(self):
        for course in self.courses_attached:
            self.average_grade.append(sum(self.grades[course])/len(
                self.grades[course]))
        return sum(self.average_grade)/len(self.average_grade) if len(
            self.average_grade) > 0 else 0

    def __str__(self):
        return (f'Имя: {self.name}\nФамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.__grade_total()}')

    def __lt__(self, other):
        return self.__grade_total() < other.__grade_total()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


student_1 = Student('Даниил', 'Чувызгалов', 'Мужской')
student_1.finished_courses += ['Python', 'Git']
student_1.courses_in_progress += ['ООП и работа с API']
student_1.grades['Python'] = [7]
student_1.grades['Git'] = [9]

student_2 = Student('Алёна', 'Иванова', 'Женский')
student_2.finished_courses += ['Python', 'Git']
student_2.courses_in_progress += ['ООП и работа с API']
student_2.grades['Python'] = [6]
student_2.grades['Git'] = [8]

lecturer_1 = Lecturer('Олег', 'Булыгин')
lecturer_1.courses_attached += ['ООП и работа с API']

reviewer_1 = Reviewer('Александр', 'Бардин')
reviewer_1.courses_attached += ['ООП и работа с API']

lecturer_2 = Lecturer('Дмитрий', 'Демидов')
lecturer_2.courses_attached += ['ООП и работа с API']

reviewer_2 = Reviewer('Дарья', 'Шиханова')
reviewer_2.courses_attached += ['ООП и работа с API']

student_1.rate_lec(lecturer_1, 'ООП и работа с API', 10)
student_1.rate_lec(lecturer_2, 'ООП и работа с API', 10)

student_2.rate_lec(lecturer_1, 'ООП и работа с API', 10)
student_2.rate_lec(lecturer_2, 'ООП и работа с API', 9)

reviewer_1.rate_hw(student_1, 'ООП и работа с API', 8)
reviewer_1.rate_hw(student_2, 'ООП и работа с API', 7)

reviewer_2.rate_hw(student_1, 'ООП и работа с API', 7)
reviewer_2.rate_hw(student_2, 'ООП и работа с API', 9)

print(f'Список студентов: \n{student_1}\n\n{student_2}\n')
print(f'Список экспертов: \n{reviewer_1}\n\n{reviewer_2}\n')
print(f'Список лекторов: \n{lecturer_1}\n\n{lecturer_2}\n')


def grade_hw(students, course):
    for student in students:
        if (course in student.courses_in_progress
                or course in student.finished_courses):
            return sum(student.grades[course])/len(student.grades[course])


def grade_lec(lecturers, course):
    for lecturer in lecturers:
        if course in lecturer.courses_attached:
            return sum(lecturer.grades[course])/len(lecturer.grades[course])


def max_grade_student(student1, student2):
    if student1.__lt__(student2):
        return f'{student2.name} {student2.surname}'
    else:
        return f'{student1.name} {student1.surname}'


def max_grade_lecturer(lecturer1, lecturer2):
    if lecturer1.__lt__(lecturer2):
        return f'{lecturer2.name} {lecturer2.surname}'
    else:
        return f'{lecturer1.name} {lecturer1.surname}'


print(f'Обладатель наивысшего среднего балла за домашние задания по курсу '
      f'"ООП и работа с API": {max_grade_student(student_1, student_2)}')

print(f'Обладатель наивысшего среднего балла за лекции в рамках курса '
      f'"ООП и работа с API": {max_grade_lecturer(lecturer_1, lecturer_2)}')

test_course_hw = 'ООП и работа с API'
test_students_hw = [student_1, student_2]
print(f'Средняя оценка за домашние задания по курсу "{test_course_hw}": '
      f'{grade_hw(test_students_hw, test_course_hw)}')

test_course_lec = 'ООП и работа с API'
test_lecturers_lec = [lecturer_1, lecturer_2]
print(f'Средняя оценка за лекции в рамках курса "{test_course_lec}": '
      f'{grade_lec(test_lecturers_lec, test_course_lec)}')
