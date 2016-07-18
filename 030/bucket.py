from datetime import datetime, timedelta

def test(bucket, amount):
    if bucket.deduct(amount):
        print 'Had %s quota' % amount
    else:
        print 'Not enough for %s quota' % amount


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.utcnow()
        self.max_quota = 0
        self.quota_consumed = 0

    def fill(self, amount):
        now = datetime.utcnow()
        if now - self.reset_time >  self.period_delta:
            self.quota = 0
            self.reset_time = now
        self.quota += amount

    def deduct(self, amount):
        now = datetime.utcnow()
        if now - self.reset_time >  self.period_delta:
            return False
        if self.quota - amount < 0:
            return False
        self.quota -= amount
        return True

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - self.quota_consumed
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

    def __repr__(self):
        return 'Bucket(max_quota=%d, quota_consumed=%d)' % \
               (self.max_quota, self.quota_consumed)

