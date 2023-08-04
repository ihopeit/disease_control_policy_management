from django.core.management.base import BaseCommand

from policies.models import DiseaseType

disease_names = [
    "鼠疫", "霍乱", "传染性非典型肺炎( 甲管 )", "艾滋病", "病毒性肝炎", "脊髓灰质炎", "人感染高致病性禽流感", "麻疹", "流行性出血热", "狂犬病", "流行性乙型脑炎",
    "登革热", "炭疽(肺炭疽为甲管)", "细菌性和阿米巴性痢疾", "肺结核", "伤寒和副伤寒", "流行性脑脊髓膜炎", "百日咳", "白喉", "新生儿破伤风", "猩红热", "布鲁氏菌病",
    "淋病", "梅毒", "钩端螺旋体病", "血吸虫病", "疟疾", "人感染H7N9禽流感", "新型冠状病毒感染", "流行性感冒", "流行性腮腺炎", "风疹", "急性出血性结膜炎",
    "麻风病", "斑疹伤寒", "黑热病", "包虫病", "丝虫病", "其他感染性腹泻病", "手足口病", "其他", "综合", "肠道传染病", "呼吸道传染病", "自然疫源性传染病",
    "虫媒传染病", "血源及性传播传染病"
]


class Command(BaseCommand):
    help = 'Initialize DiseaseType table with predefined disease names'

    def handle(self, *args, **options):
        for name in disease_names:
            DiseaseType.objects.create(name=name)

        self.stdout.write(self.style.SUCCESS('Disease types initialized successfully.'))