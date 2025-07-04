# booking_api/utils.py
from datetime import datetime
from pytz import timezone, all_timezones
from schemas import ClassResponse

def convert_class_times(classes: list[ClassResponse], target_tz: str) -> list[ClassResponse]:
    """
    Convert class datetime fields from IST to the requested timezone.

    Parameters:
        classes (List[ClassResponse]): List of class entries.
        target_tz (str): Target timezone (e.g., 'UTC', 'America/New_York').

    Returns:
        List[ClassResponse]: Classes with datetime converted.
    """
    if target_tz not in all_timezones:
        raise ValueError(f"Invalid timezone: {target_tz}")

    ist = timezone("Asia/Kolkata")
    target = timezone(target_tz)

    converted_classes = []

    for cls in classes:
        # Parse stored datetime as IST
        original_time = ist.localize(datetime.fromisoformat(cls.datetime))
        converted_time = original_time.astimezone(target)

        converted_classes.append(
            ClassResponse(
                id=cls.id,
                name=cls.name,
                datetime=converted_time.isoformat(),
                instructor=cls.instructor,
                slots=cls.slots
            )
        )

    return converted_classes
