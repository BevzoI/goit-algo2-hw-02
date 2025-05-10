from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Сортування: за пріоритетом (1 найвищий), далі за довшим часом (жадібно)
    jobs.sort(key=lambda job: (job.priority, -job.print_time))

    print_order = []
    total_time = 0
    i = 0
    n = len(jobs)
    batch_num = 1

    while i < n:
        group = []
        total_volume = 0
        count = 0
        j = i

        # Спробуємо зібрати групу, не порушуючи обмеження принтера
        while j < n and count < printer.max_items and total_volume + jobs[j].volume <= printer.max_volume:
            group.append(jobs[j])
            total_volume += jobs[j].volume
            count += 1
            j += 1

        if not group:
            # Якщо нічого не вдалося додати до групи — друкуємо окремо
            job = jobs[i]
            print(f"Група {batch_num}: {job.id} (індивідуально, перевищення обмежень)")
            print_order.append(job.id)
            total_time += job.print_time
            i += 1
        else:
            # Додаємо групу до порядку друку
            group_ids = [job.id for job in group]
            group_time = max(job.print_time for job in group)
            print(f"Група {batch_num}: {group_ids} (час: {group_time} хв, обʼєм: {total_volume} см³)")
            print_order.extend(group_ids)
            total_time += group_time
            i += len(group)
        batch_num += 1

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    tests = [
        {
            "name": "Тест 1 (однаковий пріоритет)",
            "jobs": [
                {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
                {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
                {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
            ]
        },
        {
            "name": "Тест 2 (різні пріоритети)",
            "jobs": [
                {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
                {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
                {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
            ]
        },
        {
            "name": "Тест 3 (перевищення обмежень)",
            "jobs": [
                {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
                {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
                {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
            ]
        }
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    for test in tests:
        print(f"\n=== {test['name']} ===")
        result = optimize_printing(test["jobs"], constraints)
        print(f"\nПорядок друку: {result['print_order']}")
        print(f"Загальний час друку: {result['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
