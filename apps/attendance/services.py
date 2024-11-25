from datetime import datetime, time
from .models import Attendance, LeaveBalance


def process_attendance(user, check_in=None, check_out=None):
    """
    Create or update the Attendance record for the user performing the action.
    """
    today = datetime.today().date()
    attendance, created = Attendance.objects.get_or_create(user=user, date=today)

    if check_in:
        attendance.check_in = check_in
        if attendance.is_late:
            try:
                leave_balance = LeaveBalance.objects.get(user=user)
            except LeaveBalance.DoesNotExist:
                # If the user doesn't have a leave balance, create one
                leave_balance = LeaveBalance.objects.create(user=user)

            leave_balance.deduct_leave(attendance.late_minutes)
        attendance.save()

    # Calculate overtime if check_out is provided
    if check_out:
        attendance.check_out = check_out
        attendance.calculate_overtime()
        attendance.save()

    return attendance
