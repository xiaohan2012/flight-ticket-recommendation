from faker import Faker
fake = Faker('zh_CN')
for i in range(10):
    print(fake.name())
