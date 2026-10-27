
from browser import document, html


class RMAAnalyzer:
    def __init__(self):
        self.tasks = []
        document["add"].bind("click", self.add_task)
        document["clear"].bind("click", self.clear_all)
        document["execution"].bind("keydown", self.on_enter)
        document["period"].bind("keydown", self.on_enter)

    def analyze(self):
        if not self.tasks:
            return {"utilization": 0, "bound": 0, "sufficient": True}
        utilization = sum(task["execution"] / task["period"] for task in self.tasks)
        n = len(self.tasks)
        bound = n * (2 ** (1 / n) - 1)
        return {"utilization": utilization, "bound": bound, "sufficient": utilization <= bound}

    def render_tasks(self):
        area = document["tasks"]
        area.clear()
        if not self.tasks:
            area <= html.DIV("No tasks added yet.", Class="empty")
            return

        header = html.DIV(Class="task task-header")
        header <= html.DIV("Task", Class="task-column task-info")
        header <= html.DIV("Execution Time (C)", Class="task-column")
        header <= html.DIV("Period (T)", Class="task-column")
        area <= header

        for task in self.tasks:
            row = html.DIV(Class="task")
            info = html.DIV(Class="task-column task-info")
            info <= html.DIV(task["name"], Class="task-name")
            info <= html.DIV("Periodic task", Class="task-subtitle")

            execution = html.DIV(Class="task-column")
            execution <= html.SPAN(f'{task["execution"]:g} ms', Class="value-number")

            period = html.DIV(Class="task-column")
            period <= html.SPAN(f'{task["period"]:g} ms', Class="value-number")

            row <= info
            row <= execution
            row <= period
            area <= row

    def render_analysis(self):
        output = document["result"]
        output.clear()
        if not self.tasks:
            output <= html.DIV("Add a task to begin analysis.", Class="empty")
            return

        result = self.analyze()
        metrics = [
            ("CPU Utilization", f'{result["utilization"] * 100:.2f}%'),
            ("RMS Utilization Bound", f'{result["bound"] * 100:.2f}%')
        ]
        for label, value in metrics:
            metric = html.DIV(Class="metric")
            metric <= html.SPAN(label, Class="metric-label")
            metric <= html.SPAN(value, Class="metric-value")
            output <= metric

        passed = result["sufficient"]
        status = html.DIV(Class="status " + ("status-pass" if passed else "status-fail"))
        status <= html.SPAN("Sufficient Test")
        status <= html.SPAN("PASS" if passed else "FAIL")
        output <= status

    def on_enter(self, event):
        if event.key == "Enter":
            event.preventDefault()
            self.add_task(event)

    def show_error(self, message):
        output = document["result"]
        output.clear()
        output <= html.DIV(message, Class="empty")

    def add_task(self, event):
        try:
            execution = float(document["execution"].value)
            period = float(document["period"].value)
        except (ValueError, TypeError):
            self.show_error("Enter valid numeric values.")
            return

        if execution <= 0 or period <= 0 or execution > period:
            self.show_error("Require 0 < execution time <= period.")
            return

        self.tasks.append({"name": f"P{len(self.tasks) + 1}", "execution": execution, "period": period})
        document["execution"].value = ""
        document["period"].value = ""
        self.render_tasks()
        self.render_analysis()
        document["execution"].focus()

    def clear_all(self, event):
        self.tasks.clear()
        document["execution"].value = ""
        document["period"].value = ""
        self.render_tasks()
        self.render_analysis()
        document["execution"].focus()


app = RMAAnalyzer()
