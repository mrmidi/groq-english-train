from task_handler import DirectToIndirectSpeechTaskHandler
class TaskFactory:
    @staticmethod
    def get_task_handler(task_type):
        # Mapping of task type names to their corresponding handler classes
        task_mapping = {
            'direct_to_indirect_speech': DirectToIndirectSpeechTaskHandler,
            # Additional task types can be added here as new classes are implemented
        }

        if task_type in task_mapping:
            return task_mapping[task_type]()
        else:
            raise ValueError(f"Unknown task type: {task_type}")


# Example usage (for internal testing or module verification)
if __name__ == "__main__":
    try:
        task_handler = TaskFactory.get_task_handler('direct_to_indirect_speech')
        print(task_handler.fetch_task())  # Outputs the task for debugging purposes
    except ValueError as error:
        print(error)
