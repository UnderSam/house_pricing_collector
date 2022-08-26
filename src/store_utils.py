
from typing import List, Dict, Any
from multiprocessing import Manager


class StoreProcedure():
    def __init__(self) -> None:
        manager = Manager()
        self.collected_results = manager.list()
        self.failed_tasks = manager.list()
    
    def insert_result(self, record: Dict[str, Any]) -> None:
        self.collected_results.append(record)

    def insert_failed(self, record: Dict[str, Any]) -> None:
        self.failed_tasks.append(record)
    
    def get_collected_results(self) -> List[Dict[str, Any]]:
        return list(self.collected_results)

    def get_collected_faileds(self) -> List[Dict[str, Any]]:
        return list(self.failed_tasks)
