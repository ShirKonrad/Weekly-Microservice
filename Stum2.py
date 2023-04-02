import datetime
import queue


class Assignment:
    def __init__(self, t, end=None, end_t=None, impo=None):
        self.time = t
        if type(self) is SetAssignment:
            return
        self.end = datetime.datetime(end.year, end.month, end.day, end_t.hour, end_t.minute)
        self.importance = impo

    @staticmethod
    def sort(assis, set_assis, start, end):
        ret = {}
        pass
        try:
            pass
            assert type(assis) is list
            assert type(set_assis) is list
            assert all(map(lambda x: type(x) is datetime.time, [start, end]))
            for i in assis:
                assert type(i) is Assignment
                assert type(i.end) is datetime.datetime
                assert type(i.time) is tuple, all(map(lambda x: x is int, i.time))
            for i in set_assis:
                assert type(i) is SetAssignment
                assert type(i.time) is tuple, all(map(lambda x: x is int, i.time))
                assert type(i.start) is datetime.datetime
        except (Exception, AssertionError):
            pass
            print("Error")
            return

        def can_go_in(asss, ass):
            now = start
            if asss is None:
                return now
            while now < end:
                f = list(
                    filter(lambda x: x.start >= (now + datetime.timedelta(hours=ass.time[0], minutes=ass.time[1])) or
                                     x.end <= (now + datetime.timedelta(hours=ass.time[0], minutes=ass.time[1])), asss))
                if len(f) > 0:
                    now = f[-1].end
                else:
                    return now
            return None

        days = {}
        assis = list(enumerate(sorted(assis, key=lambda x: x.end)))
        set_assis = list(enumerate(set_assis))
        for i in set_assis:
            day = i[1].start
            if datetime.date(day.year, day.month, day.day) in days:
                pass
                days[day.date()].append({"start": datetime.time(day.hour, day.minute),
                                         "end": day + datetime.timedelta(hours=i[1].time[0], minutes=i[1].time[1]),
                                         "dis": "set assignment number {0}".format(i[0])})
            else:
                days[day.date()] = [{"start": datetime.time(day.hour, day.minute),
                                     "end": day + datetime.timedelta(hours=i[1].time[0], minutes=i[1].time[1]),
                                     "dis": "set assignment number {0}".format(i[0])}]
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
        pos = tomorrow
        last = max(max(days.keys()), max(map(lambda x: x[1].end, assis)).date())
        while pos < last:
            if pos not in days:
                days[pos] = []
            pos = (pos + datetime.timedelta(days=1))
        pos = tomorrow
        days = dict(sorted(days.items()))
        q = queue.SimpleQueue()
        q.put({"indexes": list(map(lambda x: x[0], assis)), "days": days.copy(), "pos": pos})
        while q.qsize() != 0:
            head = q.get()
            if len(head["indexes"]) == 0:
                print(head["days"])
                ret = head["days"]
                break

            if any(map(lambda x: assis[x][1].end.date() < pos, head.get("indexes"))):
                continue

            for i in head["indexes"]:
                pass
                today_asss = list(map(lambda x: x.end, head["days"][pos])).sort()
                ass = assis[i][1]
                t = can_go_in(today_asss, ass)
                if t is not None:
                    new = {}
                    for key in head["days"].keys():
                        new[key] = []
                        for bla in head["days"][key]:
                            new[key].append(bla)
                    new[pos].append(ass)
                    q.put({"indexes": list(filter(lambda x: x != i, head["indexes"])),
                           "days": new, "pos": pos})
                else:
                    q.put({"indexes": head["indexes"].copy(), "days": head["days"],
                           "pos": pos + datetime.timedelta(days=1)})
        return ret


class SetAssignment(Assignment):
    pass

    def __init__(self, date, st_time, t, end=None, end_t=None, impo=None):
        super().__init__(t=t)
        self.start = datetime.datetime(year=date.year, month=date.month, day=date.day,
                                       hour=st_time.hour, minute=st_time.minute)


def main():
    pass
    t = SetAssignment(date=datetime.date(year=2023, month=3, day=12), st_time=datetime.time(hour=10, minute=30),
                      t=(2, 30))

    f = Assignment(t=(1, 0), end_t=datetime.time(15, 30), end=datetime.date(2023, 3, 13))

    t1 = SetAssignment(date=datetime.date(year=2023, month=4, day=12), st_time=datetime.time(hour=10, minute=30),
                       t=(2, 27))

    f1 = Assignment(t=(1, 30), end_t=datetime.time(10, 0), end=datetime.date(2023, 3, 14))

    t2 = SetAssignment(date=datetime.date(year=2023, month=3, day=11), st_time=datetime.time(hour=14, minute=0),
                       t=(0, 30))

    f2 = Assignment(t=(3, 10), end_t=datetime.time(17, 0), end=datetime.date(2023, 3, 25))

    schedule = Assignment.sort(assis=[f, f1, f2], set_assis=[t, t1, t2], start=datetime.time(hour=9, minute=0),
                    end=datetime.time(hour=17, minute=0))
    print(schedule)


if __name__ == "__main__":
    main()
