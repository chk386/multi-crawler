from functools import wraps
from typing import no_type_check


@no_type_check
def throttle(delay: int):
    """
    함수 호출을 지정된 시간(delay) 간격으로 제한하는 데코레이터
    """

    @no_type_check
    def decorator(func):
        last_call_time = 0
        scheduled_id = None

        @wraps(wrapped=func)
        @no_type_check
        def wrapper(self, *args, **kwargs):
            nonlocal last_call_time, scheduled_id

            current_time = time.time() * 1000

            # 이전에 예약된 호출이 있으면 취소
            if scheduled_id is not None:
                self.after_cancel(scheduled_id)
                scheduled_id = None

            # 마지막 호출 이후 delay보다 시간이 지났는지 확인
            if current_time - last_call_time > delay:
                # 충분한 시간이 지났으면 즉시 호출
                func(self, *args, **kwargs)
                last_call_time = current_time
            else:
                # 그렇지 않으면 호출을 예약
                scheduled_id = self.after(delay, lambda: func(self, *args, **kwargs))

        return wrapper

    return decorator
