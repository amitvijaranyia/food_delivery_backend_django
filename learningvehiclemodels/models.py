from datetime import datetime

from django.contrib.gis.db.models import PointField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
# from parkwheels_vehicle.logging.app_logger import AppLogger
# from utils import helper as parkplus_utils
# from jsonfield import JSONField
# from simple_history.models import HistoricalRecords


# logger = AppLogger(tag="vehicle model views")


# Create your models here.
def get_upload_path(instance, filename):
    import os
    from django.utils.timezone import now

    filename_base, filename_ext = os.path.splitext(filename)
    return "%s%s%s" % (
        instance.recipe.user.username,
        now().strftime("%Y%m%d%H%M%S") + str(now().microsecond),
        filename_ext.lower(),
    )


class CommonModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vehicle(CommonModel):
    TWO_WHEELER = 2
    THREE_WHEELER = 3
    FOUR_WHEELER = 4
    SIX_WHEELER = 6
    EIGHT_WHEELER = 8

    WHEEL_COUNT = (
        (TWO_WHEELER, "two wheeler"),
        (THREE_WHEELER, "three wheeler"),
        (FOUR_WHEELER, "four wheeler"),
        (SIX_WHEELER, "six wheeler"),
        (EIGHT_WHEELER, "eight wheeler"),
    )

    PRIVATE = 0
    COMMERCIAL = 1
    PUBLIC = 2
    GOVERNMENT = 3
    DEFENCE = 4

    VEHICLE_CATEGORY = (
        (PRIVATE, "Private"),
        (COMMERCIAL, "Commercial"),
        (PUBLIC, "Public"),
        (GOVERNMENT, "Government"),
        (DEFENCE, "Defence"),
    )

    PETROL = 0
    DIESEL = 1
    CNG = 2
    ELECTRIC = 3
    HYBRID = 4

    FUEL_TYPES = (
        (PETROL, "Petrol"),
        (DIESEL, "Diesel"),
        (CNG, "CNG"),
        (ELECTRIC, "Electric"),
        (HYBRID, "Hybrid"),
    )

    UNVERIFIED = 0
    INITIATED = 1
    INPROGRESS = 2
    VERIFIED = 3
    FAILED = 4

    VERIFICATION_TYPES = (
        (UNVERIFIED, "Unverified"),
        (INITIATED, "Initiated"),
        (INPROGRESS, "In Progress"),
        (VERIFIED, "Verified"),
        (FAILED, "Failed"),
    )

    PER_DAY_KM = (
        ("0-10", "0-10 Kms"),
        ("10-25", "10-25 Kms"),
        ("25-50", "25-50 Kms"),
        ("50-75", "50-75 Kms"),
        ("75+", "75+ Kms"),
    )

    CAR = 0
    MOTORCYCLE = 1

    VEHICLE_TYPE = ((CAR, "Car"), (MOTORCYCLE, "Motorcycle"))

    UNVERIFIED = 0
    VERIFIED = 1
    SEMI_VERIFIED = 2
    SECONDARY_REQUESTED = 3
    SECONDARY_APPROVED = 4
    SECONDARY_REJECTED = 5
    ADDED_FOR_SOME_ELSE = 6
    SECONDARY_PENDING = 7
    SECONDARY_NOTREQUESTED = 8
    FOR_REMINDER = 9

    USER_VEHICLE_STATUS = (
        (UNVERIFIED, "Unverified"),
        (VERIFIED, "Verified"),
        (SEMI_VERIFIED, "Semi Verified"),
        (SECONDARY_REQUESTED, "Secondary Requested"),
        (SECONDARY_APPROVED, "Secondary Approved"),
        (SECONDARY_REJECTED, "Secondary Rejected"),
        (ADDED_FOR_SOME_ELSE, "Added for some one else"),
        (SECONDARY_PENDING, "Secondary Pending"),
        (SECONDARY_NOTREQUESTED, "Secondary Not Requested"),
        (FOR_REMINDER, "For Reminder"),
    )

    VEHICLE_SOURCE_B2C = "B2C"
    VEHICLE_SOURCE_CHALLAN = "CHALLAN"
    VEHICLE_SOURCE_FASTTAG = "FASTAG"
    VEHICLE_SOURCE_DIGILOCKER = "DIGILOCKER"
    VEHICLE_SOURCE_PASS = "PASS"
    VEHICLE_SOURCE_MG_MOTORS = "MG-MOTORS"

    VEHICLE_SOURCES = (
        (VEHICLE_SOURCE_B2C, "B2C"),
        (VEHICLE_SOURCE_CHALLAN, "CHALLAN"),
        (VEHICLE_SOURCE_FASTTAG, "FASTAG"),
        (VEHICLE_SOURCE_DIGILOCKER, "DIGILOCKER"),
        (VEHICLE_SOURCE_PASS, "PASS"),
        (VEHICLE_SOURCE_MG_MOTORS,"MG-MOTORS")
    )

    VEHICLE_VERIFY_USER = "USER"
    VEHICLE_VERIFY_DIGILOCKER = "DIGILOCKER"
    VEHICLE_VERIFY_SUPERTAG = "SUPERTAG"

    VEHICLE_VERIFY_SOURCES = (
        (VEHICLE_VERIFY_USER, "USER"),
        (VEHICLE_VERIFY_DIGILOCKER, "DIGILOCKER"),
        (VEHICLE_VERIFY_SUPERTAG, "SUPERTAG"),
    )

    MANUAL = 0
    AUTOMATIC = 1

    TRANSMISSION_TYPES = ((MANUAL, "Manual"), (AUTOMATIC, "Automatic"))

    license = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    temp_license = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    wheel_count = models.PositiveIntegerField(choices=WHEEL_COUNT, null=True, blank=True)
    vehicle_category = models.PositiveIntegerField(choices=VEHICLE_CATEGORY, null=True, blank=True)
    vehicle_type = models.PositiveIntegerField(choices=VEHICLE_TYPE, null=True, blank=True)
    transmission = models.PositiveIntegerField(choices=TRANSMISSION_TYPES, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    year_of_purchase = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.PositiveIntegerField(choices=FUEL_TYPES, null=True, blank=True)
    per_day_km = models.CharField(choices=PER_DAY_KM, null=True, blank=True, max_length=20)
    reg_date = models.DateTimeField(blank=True, null=True)
    insurance_expiry = models.DateTimeField(blank=True, null=True)
    last_service = models.DateTimeField(blank=True, null=True)
    verification = models.PositiveIntegerField(choices=VERIFICATION_TYPES, null=True, blank=True)
    # meta_data = JSONField(default={}, blank=True, null=True)
    registered_on_app = models.BooleanField(null=True, blank=True)
    user_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    default = models.BooleanField(null=True, blank=True)
    sequence = models.PositiveIntegerField(null=True, blank=True)
    user_vehicle_status = models.PositiveIntegerField(choices=USER_VEHICLE_STATUS, null=True, blank=True)
    vehicle_other_phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="phone number of the user for which some user added vehicle",
    )
    # challan_other_notify_data = JSONField(default={}, blank=True, null=True)
    active = models.BooleanField(default=True)
    source = models.CharField(max_length=255, null=True, blank=True, choices=VEHICLE_SOURCES)
    verified_by = models.CharField(max_length=255, null=True, blank=True, choices=VEHICLE_VERIFY_SOURCES)
    vin = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "vehicle"

    def get_vehicle_category(self):
        vehicle_category_dict = {
            0: "Private",
            1: "Commercial",
            2: "Public",
            3: "Government",
            4: "Defence",
        }
        return vehicle_category_dict.get(self.vehicle_category)

    def get_fuel_type(self):
        fuel_type_dict = {
            0: "Petrol",
            1: "Diesel",
            2: "Cng",
            3: "Electric",
            4: "Hybrid",
        }
        return fuel_type_dict.get(self.fuel_type)

    def get_verification_type(self):
        verification_dict = {
            0: "Unverified",
            1: "Initiated",
            2: "Inprogress",
            3: "Verified",
            4: "Failed",
        }
        return verification_dict.get(self.verification)

    def get_vehicle_type(self):
        vehicle_type_dict = dict(self.VEHICLE_TYPE)
        return vehicle_type_dict.get(self.vehicle_type)

    @property
    def transmission_display(self):
        if not self.transmission:
            return
        transmission_type_dict = dict(self.TRANSMISSION_TYPES)
        return transmission_type_dict.get(int(self.transmission))


class TagInfra(CommonModel):
    MANUAL = 0
    AUTOMATIC = 1

    FCFS = 0
    RESERVED = 1
    TEMPORARY_FCFS = 2
    TEMPORARY_RESERVED = 3

    MANUAL_ASSIGNMENT = 0
    MONOLITHIC = 1
    API = 2
    DASHBOARD = 3
    TAG_ONBOARDING = 4

    ASSIGNMENT_SOURCES = (
        (MANUAL_ASSIGNMENT, "Manual Assignment"),
        (MONOLITHIC, "Monolithic"),
        (API, "Api"),
        (DASHBOARD, "Dashboard"),
        (TAG_ONBOARDING, "TagOnboarding"),
    )

    LOCK_TYPES = (
        (MANUAL, "Manual"),
        (AUTOMATIC, "Auto"),
    )

    CHARGE_STATUS = (
        (FCFS, "General"),
        (RESERVED, "Reserved"),
    )

    NFC = 0
    RFID = 1

    TAG_TYPES = ((RFID, "RFID"), (NFC, "NFC"))

    tag_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    tag_type = models.PositiveIntegerField(choices=TAG_TYPES, null=True)
    charge_status = models.IntegerField(choices=CHARGE_STATUS, null=True, blank=True)
    wheel_count = models.PositiveIntegerField(null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    sub_category_id = models.IntegerField(null=True, blank=True)
    vehicle_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    project_id = models.PositiveIntegerField(null=True, blank=True)
    building_id = models.PositiveIntegerField(null=True, blank=True)
    company_id = models.PositiveIntegerField(null=True, blank=True)
    floor_id = models.PositiveIntegerField(null=True, blank=True)
    slot_id = models.PositiveIntegerField(null=True, blank=True)
    zone_id = models.PositiveIntegerField(null=True, blank=True)
    gate_id = models.PositiveIntegerField(null=True, blank=True)
    unit_id = models.PositiveIntegerField(null=True, blank=True)
    configuration_id = models.PositiveIntegerField(null=True, blank=True)
    emp_id = models.CharField(max_length=50, null=True, blank=True)
    default = models.BooleanField(default=False)
    sequence = models.PositiveIntegerField(default=1)
    start = models.TimeField(null=True, blank=True, help_text="lock start in case auto lock")
    end = models.TimeField(null=True, blank=True, help_text="lock end in case auto lock")
    tag_lock_feature = models.BooleanField(default=True, help_text="If feature enabled by user")
    lock_control = models.BooleanField(default=False, help_text="If the locking is activate or not")
    locked = models.BooleanField(default=False)
    primary_vehicle = models.BooleanField(default=False, help_text="Will be displayed first on home screen")
    allow_advance_booking = models.BooleanField(default=False, help_text="Allow advanced booking")
    emergency_open = models.BooleanField(default=False)
    tag_lost = models.BooleanField(default=False)
    lock_type = models.PositiveIntegerField(choices=LOCK_TYPES, null=True, blank=True)
    tag_expiry = models.DateTimeField(null=True, blank=True)
    assignment_source = models.PositiveIntegerField(choices=ASSIGNMENT_SOURCES, null=True, blank=True)
    active = models.BooleanField(default=True)
    order_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "tag_infra"

    def get_charge_status(self):
        charge_status_dict = dict(self.CHARGE_STATUS)
        return charge_status_dict[self.charge_status] if self.charge_status else None

    def get_tag_type(self):
        tag_type_dict = dict(self.TAG_TYPES)
        return tag_type_dict[self.tag_type] if self.tag_type else None


class TagInfraGateMapping(models.Model):
    tag_infra_id = models.PositiveIntegerField(db_index=True)
    gate_id = models.PositiveIntegerField()
    tag_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tag_infra_gate_mapping"


class Tag(CommonModel):
    PARKWHEELS = 0
    OTHERS = 1
    PARKPLUS = 2
    NONPARKPLUS = 3
    IDFC_FASTAG = 4
    IDBI_FASTAG = 5
    TAG_SOURCE = (
        (PARKWHEELS, "Parkwheels"),
        (OTHERS, "Others"),
        (PARKPLUS, "Parkplus"),
        (NONPARKPLUS, "Non Parkplus"),
        (IDFC_FASTAG, "IDFC Fastag"),
        (IDBI_FASTAG, "IDBI Fastag")
    )

    NFC = 0
    RFID = 1

    TAG_TYPES = ((NFC, "nfc"), (RFID, "rfid"))

    HANDHELD = 0
    WINDSHIELD = 1

    TAG_CATEGORY = ((HANDHELD, "Handheld"), (WINDSHIELD, "Windshield"))

    MANUAL_ASSIGNMENT = 0
    MONOLITHIC = 1
    TAG_ONBOARDING = 2

    ASSIGNMENT_SOURCES = (
        (MANUAL_ASSIGNMENT, "Manual Assignment"),
        (MONOLITHIC, "Monolithic"),
        (TAG_ONBOARDING, "TagOnboarding"),
    )

    tag_id = models.CharField(max_length=255, null=True, blank=True, db_index=True, unique=True)
    tag_id2 = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    np_tag_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)  # non parkplus tag_id
    tag_secret_code = models.CharField(max_length=255, null=True, blank=True)
    tag_category = models.PositiveIntegerField(choices=TAG_CATEGORY, null=True, blank=True)
    source = models.PositiveIntegerField(choices=TAG_SOURCE, null=True)
    tid = models.CharField(max_length=255, null=True, blank=True)
    tag_type = models.PositiveIntegerField(choices=TAG_TYPES, null=True)
    # meta_data = JSONField(default={}, blank=True, null=True)
    epc_code = models.CharField(max_length=255, null=True, blank=True)
    tag_id_md5 = models.CharField(max_length=64, null=True, blank=True)
    tag_id2_md5 = models.CharField(max_length=64, null=True, blank=True)
    secret_code_md5 = models.CharField(max_length=64, null=True, blank=True)
    assignment_source = models.PositiveIntegerField(choices=ASSIGNMENT_SOURCES, null=True, blank=True)
    partner_enabled = models.BooleanField(default=False)
    partner_name = models.CharField(max_length=255, null=True, blank=True)
    is_supertag = models.BooleanField(default=False)
    bar_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "tags"

    def get_tag_source(self):
        tag_source_dict = dict(self.TAG_SOURCE)
        return tag_source_dict[self.source] if self.source else None

    def get_tag_type(self):
        tag_type_dict = dict(self.TAG_TYPES)
        return tag_type_dict[self.tag_type] if self.tag_type else None


class TagRequest(models.Model):
    REQUEST = 0
    VERIFIED = 1
    ACCEPTED = 2
    PROCESSING = 3
    DELIVERED = 4
    DECLINED = 5

    STATUS = (
        (REQUEST, "Requested"),
        (VERIFIED, "Verified"),
        (ACCEPTED, "Accepted"),
        (PROCESSING, "Out for delivery"),
        (DELIVERED, "Delivered"),
        (DECLINED, "Declined"),
    )

    PAYMENT_MODE = (("cod", "Cash on delivery"),)

    order_id = models.IntegerField(unique=True)
    user_id = models.PositiveIntegerField(null=True, blank=True)
    license = models.CharField(max_length=11, null=True, blank=True)
    referral_code = models.CharField(max_length=8, null=True, blank=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE, default=PAYMENT_MODE[0][0])
    amount = models.IntegerField(null=True, blank=True)
    status = models.PositiveIntegerField(choices=STATUS, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "tag_request"


class TagInfraLockDays(models.Model):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

    DAY_CHOICES = (
        (0, "Sunday"),
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
    )

    day_id = models.PositiveIntegerField(choices=DAY_CHOICES, null=True)
    tag_infra_id = models.PositiveIntegerField(null=True, db_index=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "tag_infra_lock_days"

    def get_lock_days(self):
        lock_day_queryset = TagInfraLockDays.objects.filter(id=self.tag_infra_id).distinct()
        lock_day_list = list(lock_day_queryset)

        return lock_day_list


class UserVehicle(models.Model):
    UNVERIFIED = 0
    VERIFIED = 1
    SEMI_VERIFIED = 2
    SECONDARY_REQUESTED = 3
    SECONDARY_APPROVED = 4
    SECONDARY_REJECTED = 5
    ADDED_FOR_SOME_ELSE = 6

    USER_VEHICLE_STATUS = (
        (UNVERIFIED, "Unverified"),
        (VERIFIED, "Verified"),
        (SEMI_VERIFIED, "Semi Verified"),
        (SECONDARY_REQUESTED, "Secondary Requested"),
        (SECONDARY_APPROVED, "Secondary Approved"),
        (SECONDARY_REJECTED, "Secondary Rejected"),
        (ADDED_FOR_SOME_ELSE, "Added for some one else"),
    )
    user_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    vehicle_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    default = models.BooleanField(default=False)
    sequence = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)
    status = models.PositiveIntegerField(null=True, choices=USER_VEHICLE_STATUS)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user_vehicle"


class UserTag(models.Model):
    user_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    tag_id = models.CharField(null=True, blank=True, max_length=255, db_index=True)
    tag_code = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "user_tag"


class VehicleAudit(models.Model):
    ADD_VEHICLE = 0
    EDIT_VEHICLE = 1
    ACTIVATE_VEHICLE = 2
    DELETE_VEHICLE = 3
    DEACTIVATE_VEHICLE = 4
    LOCK_VEHICLE = 5
    CHANGE_TAG_TYPE = 6
    LOST_TAG = 7
    CHANGE_CATEGORY = 8
    REMOVE_LOST_TAG = 9
    EDIT_TAG = 10
    ACTIVATE_TAG = 11
    DEACTIVATE_TAG = 12
    ADD_TAG = 13
    UNLOCK_VEHICLE = 14
    RETURN_TAG_CORPORATE = 15
    ADD_PASS = 16
    RENEW_PASS = 17
    UPDATE_PASS = 18
    DELETE_PASS = 19

    AUDIT_TYPES = (
        (ADD_VEHICLE, "Add Vehicle"),
        (EDIT_VEHICLE, "Edit Vehicle"),
        (ACTIVATE_VEHICLE, "Activate Vehicle"),
        (DELETE_VEHICLE, "Delete Vehicle"),
        (DEACTIVATE_VEHICLE, "Deactivate Vehicle"),
        (LOCK_VEHICLE, "Lock Vehicle"),
        (CHANGE_TAG_TYPE, "Change Tag Type"),
        (LOST_TAG, "Lost Tag"),
        (CHANGE_CATEGORY, "Change Category"),
        (REMOVE_LOST_TAG, "Remove Lost Tag"),
        (EDIT_TAG, "Edit Tag"),
        (ACTIVATE_TAG, "Activate Tag"),
        (ADD_TAG, "Add Tag"),
        (DEACTIVATE_TAG, "Deactivate Tag"),
        (UNLOCK_VEHICLE, "Unlock Vehicle"),
        (RETURN_TAG_CORPORATE, "Corporate Tags Returned"),
        (ADD_PASS, "Add Pass"),
        (RENEW_PASS, "Renew Pass"),
        (UPDATE_PASS, "Update Pass"),
        (DELETE_PASS, "Delete Pass"),
    )

    PENDING = 0
    DONE = 1
    HARDWARE_ACK = 2
    FAILED = 3

    AUDIT_STATUS = ((PENDING, "Pending"), (DONE, "Done"), (HARDWARE_ACK, "Hardware acknowledged"), (FAILED, "Failed"))

    project_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    company_id = models.PositiveIntegerField(null=True, blank=True)
    vehicle_id = models.IntegerField(null=True, db_index=True)
    tag_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    audit_type = models.PositiveIntegerField(null=True, choices=AUDIT_TYPES)
    action_id = models.PositiveIntegerField(null=True)
    action_by_id = models.IntegerField(blank=True, null=True, help_text="action by userid")
    status = models.PositiveIntegerField(choices=AUDIT_STATUS, null=True)
    remarks = models.TextField(blank=True, null=True)
    # dump = JSONField(default={}, blank=True, null=True)
    pass_id = models.PositiveIntegerField(null=True, blank=True)
    level = models.IntegerField(default=1, help_text="Level for permissions: 1-highest", null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vehicle_audit"

    def get_status(self):
        status_dict = {0: "Pending", 1: "Done"}

        return status_dict.get(self.status)

    def get_audit_type(self):
        audit_type_dict = dict(self.AUDIT_TYPES)
        return audit_type_dict[self.audit_type] if self.audit_type else None


class Pass(CommonModel):
    DAILY = 0
    WEEKLY = 1
    MONTHLY = 2
    QUATERLY = 3
    YEARLY = 4
    UNLIMITED = 5
    OTHERS = 6

    PASS_TYPES = (
        (DAILY, "Daily"),
        (WEEKLY, "weekly"),
        (MONTHLY, "Monthly"),
        (YEARLY, "Yearly"),
        (QUATERLY, "Quaterly"),
        (UNLIMITED, "Unlimited"),
        (OTHERS,"Others")
    )

    CAR = 0
    MOTORCYCLE = 1
    CARGO = 2

    VEHICLE_TYPES = ((CAR, "Car"), (MOTORCYCLE, "Motorcycle"), (CARGO, "Cargo"))

    INSIDER = 0
    OUTSIDER = 1

    B2C = "B2C"
    DASHBOARD = "DASHBOARD"
    MOA="MOA"
    BULK_UPLOAD="BULK_UPLOAD"

    FCFS=0
    RESERVED=1
    SLOT_TYPES=((FCFS, "FCFS"), (RESERVED, "RESERVED"))

    PASS_CATEGORIES = ((INSIDER, "Insider"), (OUTSIDER, "Outsider"))

    PAYMENT_MODES = (("CASH", "Cash"), ("PAYTM", "PAYTM"), ("UPI", "Upi"))

    RENEwED_BY_CHOICES = (("USER", "User"), ("SCRIPT", "Script"))

    PASS_SOURCES = ((B2C, "B2C"), (DASHBOARD, "DASHBOARD"),(MOA,"MOA"),(BULK_UPLOAD, "BULK_UPLOAD"))

    vehicle_type = models.PositiveIntegerField(choices=VEHICLE_TYPES, null=True)
    pass_type = models.PositiveIntegerField(choices=PASS_TYPES, null=True)
    category = models.PositiveIntegerField(choices=PASS_CATEGORIES, null=True)
    start = models.DateTimeField(null=True, blank=True, help_text="start date time of pass")
    end = models.DateTimeField(null=True, blank=True, help_text="end date time of pass")
    amount = models.IntegerField(null=True, help_text="Pass Amount")
    allowed_visits = models.IntegerField(default=30)
    visits_done = models.IntegerField(default=0)
    duration = models.IntegerField(null=True)  # in months
    valid = models.BooleanField(null=False)
    parent_id = models.PositiveIntegerField(null=True)
    # pass_invoice = JSONField(default={}, blank=True, null=True)
    auto_renew = models.BooleanField(null=True)
    # meta_data = JSONField(default={}, blank=True, null=True)
    concurrency = models.PositiveIntegerField(null=True)
    daily_limit = models.PositiveIntegerField(null=True)
    active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(null=True)
    pass_template_id = models.PositiveIntegerField(null=True, blank=True)
    pass_template_name = models.CharField(max_length=255, null=True, blank=True)
    payment_mode = models.CharField(max_length=255, null=True, blank=True, choices=PAYMENT_MODES)
    renewed_by = models.CharField(max_length=255, null=True, blank=True, choices=RENEwED_BY_CHOICES)
    source = models.CharField(max_length=255, null=True, choices=PASS_SOURCES)
    created_by_name = models.CharField(max_length=255, null=True)
    created_by_user_id = models.PositiveIntegerField(blank=True, null=True)
    pass_local_id = models.CharField(max_length=255, null=True, blank=True)
    slot_type = models.PositiveIntegerField(choices=SLOT_TYPES, null=True)
    created_time_in_mills = models.CharField(max_length=255, null=True, blank=True)
    print_count = models.IntegerField(null=True,blank=True)
    calculate_overstay = models.BooleanField(default=False)

    class Meta:
        db_table = "pass"

    def get_vehicle_type(self):
        vehicle_type_dict = dict(self.VEHICLE_TYPES)
        return vehicle_type_dict[self.vehicle_type]

    def get_pass_type(self):
        pass_type_dict = dict(self.PASS_TYPES)
        return pass_type_dict[self.pass_type]

    def get_pass_category(self):
        pass_category_dict = dict(self.PASS_CATEGORIES)
        return pass_category_dict[self.category]

    def is_valid(self):
        # this considers the grace time
        # used for checking validity at the time of entry and exit of pass vehicle

        current_datetime = datetime.now
        # current_datetime = parkplus_utils.get_current_datetime()

        if current_datetime >= self.start and current_datetime <= self.end:
            self.valid = True
            self.save()
        else:
            self.valid = False
            self.save()

        return self.valid

    def check_if_valid_for_renewal(self):

        current_datetime = datetime.now
        # current_datetime = parkplus_utils.get_current_datetime()

        if current_datetime >= self.start and current_datetime <= self.end:
            is_valid = True
        else:
            is_valid = False

        return is_valid

    @property
    def pass_wheel_count(self):
        return 4 if self.vehicle_type == Pass.CAR else 2


class VehiclePass(models.Model):
    LINKING= 0
    LINK_MANUALLY = 1
    LINKED= 2
    
    FASTAG_STATUS = ((LINKING, "Linking"), (LINK_MANUALLY, "Link_Manually"), (LINKED, "linked"))
    
    pass_id = models.PositiveIntegerField(null=True)
    vehicle_id = models.PositiveIntegerField(null=True)
    tag_id = models.CharField(max_length=255, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    fastag_status = models.PositiveIntegerField(choices=FASTAG_STATUS,default=0)
    fastag_epc_code=models.CharField(max_length=255)
    class Meta:
        db_table = "vehicle_pass"


class PassInfra(models.Model):
    pass_id = models.PositiveIntegerField(null=True)
    project_id = models.PositiveIntegerField(null=True)
    company_id = models.PositiveIntegerField(null=True)
    category_id = models.PositiveIntegerField(default=6)
    floor_id = models.PositiveIntegerField(null=True)
    building_id = models.PositiveIntegerField(null=True)
    unit_id = models.PositiveIntegerField(null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "pass_infra"


class VehicleBrand(models.Model):
    wheel_count = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    brand_icon = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "vehicle_brands"


class VehicleModel(models.Model):
    wheel_count = models.PositiveIntegerField(null=True)
    brand_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    body_type = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "vehicle_models"


class VehicleDocument(models.Model):
    AWAITED = 0
    UPLOADED = 1
    APPROVED = 2
    REJECTED = 3

    DOCUMENT_STATUS = (
        (AWAITED, "Awaited"),
        (UPLOADED, "Uploaded"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    )

    RC = 0
    PAN_CARD = 1
    DRIVING_LICENSE = 2
    AADHAR = 3
    VOTER_ID = 4
    VEHICLE = 5  # corresponding to user's vehicle image
    PASSPORT = 6
    CHASSIS_CERTIFICATE = 7
    

    DOCUMENT_TYPES = (
        (RC, "RC"),
        (PAN_CARD, "Pan card"),
        (DRIVING_LICENSE, "Driving license"),
        (AADHAR, "Aadhar Card"),
        (VOTER_ID, "Voter ID"),
        (VEHICLE, "Vehicle"),
        (PASSPORT, "Passport"),
        (CHASSIS_CERTIFICATE, "ChassisCertificate")
    )

    vehicle_id = models.PositiveIntegerField(null=True, db_index=True)
    document_url = models.CharField(max_length=255, null=True)
    status = models.PositiveIntegerField(null=True, choices=DOCUMENT_STATUS)
    document_type = models.PositiveIntegerField(null=True, choices=DOCUMENT_TYPES)
    remark = models.PositiveIntegerField(null=True, blank=True)
    # dump = JSONField(default=[])
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    doc_updated_time = models.DateTimeField(null=True, blank=True)
    doc_action_time = models.DateTimeField(null=True, blank=True)
    document_file_url = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "vehicle_document"


class VehicleExtendedDetails(models.Model):
    license = models.CharField(max_length=255, null=True, blank=True, db_index=True, unique=True)
    registration_date = models.CharField(max_length=255, null=True, blank=True)
    chassis = models.CharField(max_length=255, null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    vehicle_class = models.CharField(max_length=255, null=True, blank=True)
    fuel_type = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    fitness_dt = models.CharField(max_length=255, null=True, blank=True)
    insurance_date = models.CharField(max_length=255, null=True, blank=True)
    pollution = models.CharField(max_length=255, null=True, blank=True)
    rc_status = models.CharField(max_length=255, null=True, blank=True)
    chassis_last_char = models.CharField(max_length=255, null=True, blank=True)
    engine_last_char = models.CharField(max_length=255, null=True, blank=True)
    challan_verified = models.BooleanField(default=False)
    parivahan_verified = models.BooleanField(default=True)
    full_chassis = models.CharField(max_length=255, null=True, blank=True)
    full_engine = models.CharField(max_length=255, null=True, blank=True)
    delhi_search_challan = models.BooleanField(
        null=True, blank=True, help_text="checks if vehicle valid for delhi-flow")
    vehicle_challan_last_update = models.DateTimeField(null=True)
    owner_mobile_number = models.CharField(max_length=255, blank=True, null=True)
    skip_delhi_challan = models.BooleanField(default=False, help_text="never show pop up for delhi_challan")
    delhi_challan_notify = models.DateTimeField(
        null=True, blank=True, help_text="next pop up for delhi challan notify")
    delhi_challan_last_update = models.DateTimeField(
        null=True, blank=True, help_text="indicates the last update time of delhi challan")
    is_blacklisted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(null=True)
    variant = models.ForeignKey('Variant', null=True, blank=True, on_delete=models.SET_NULL)
    retries = models.PositiveSmallIntegerField(default=0)
    # signzy_response_data = JSONField(blank=True, null=True)
    signzy_status_code = models.PositiveIntegerField(blank=True, null=True)
    # surepass_response_data = JSONField(blank=True, null=True)
    surepass_status_code = models.PositiveIntegerField(blank=True, null=True)
    # brand_model_mapping = JSONField(blank=True, null=True)
    owner_count = models.PositiveSmallIntegerField(blank=True, null=True)
    maker_name = models.CharField(max_length=255, null=True, blank=True)
    maker_model = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    owner_count = models.PositiveSmallIntegerField(blank=True, null=True)
    maker_name = models.CharField(max_length=255, null=True, blank=True)
    maker_model = models.CharField(max_length=255, null=True, blank=True)
    new_variant_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    class Meta:
        db_table = "vehicle_extended_detail"


class VehicleInsurances(models.Model):
    ACKO = 0

    INSURANCE_PARTNER = ((ACKO, "ACKO"),)

    ACTIVE = 0
    EXPIRED = 1
    INACTIVE = 2

    INSURANCE_STATUS = (
        (ACTIVE, "Active"),
        (EXPIRED, "Expired"),
        (INACTIVE, "Inactive"),
    )

    vehicle_id = models.PositiveIntegerField(null=True, blank=True)
    user_id = models.PositiveIntegerField(null=True, blank=True)
    license = models.CharField(max_length=255, null=True, blank=True)
    insurance_id = models.PositiveIntegerField(null=True, blank=True)
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    insurance_partner = models.PositiveIntegerField(null=True, blank=True, choices=INSURANCE_PARTNER)
    insurance_type = models.PositiveIntegerField(null=True, blank=True)
    status = models.PositiveIntegerField(null=True, blank=True, choices=INSURANCE_STATUS)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "vehicle_insurances"


class VehicleReminder(models.Model):
    DAY = 0
    MONTH = 1
    HOUR = 2

    DURATION_TYPE = ((DAY, "day"), (MONTH, "month"), (HOUR, "hour"))

    reminder_type_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    reminder_date = models.DateField(null=True, blank=True)
    reminder_duration_type = models.PositiveIntegerField(choices=DURATION_TYPE, default=DAY)
    is_custom_date = models.BooleanField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)


class Meta:
    db_table = "vehicle_reminder"


class VehicleReminderType(models.Model):
    INSURANCE = 0
    PUCC = 1

    USER = "User"
    SIGNZY = "Signzy"

    REMINDER_TYPE = ((INSURANCE, "Insurance"), (PUCC, "PUCC"))
    SOURCES = ((USER, "User"), (SIGNZY, "Signzy"))

    vehicle_id = models.PositiveIntegerField(null=True, blank=True)
    reminder_type = models.PositiveIntegerField(null=True, blank=True, choices=REMINDER_TYPE)
    expiry_date = models.DateTimeField(null=True, blank=True)
    reminder_type_name = models.CharField(max_length=255, null=True, blank=True)
    # other_notify_data = JSONField(default=[])
    # reminder_duration_list = JSONField(default=[])
    reminder_url = models.CharField(max_length=255, null=True, blank=True)
    reminder_upload_url = models.CharField(max_length=255, null=True, blank=True)
    alert_disable = models.BooleanField(default=False)
    custom_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    source = models.CharField(max_length=255, choices=SOURCES, default=SOURCES[0][0])
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "vehicle_reminder_type"


class ChallanDetail(CommonModel):
    PARIVAHAN = 0
    DELHI = 1
    KARNATAKA = 2
    MAHARASHTRA = 3
    GUJARAT = 4
    HYDERABAD = 5
    THIRD_PARTY = 6
    TATPAR = 7
    RAJASTHAN = 8

    CHALLAN_DATA_SOURCE = (
        (PARIVAHAN, "Parivahan"),
        (DELHI, "Delhi"),
        (KARNATAKA, "Karnataka"),
        (MAHARASHTRA, "Maharashtra"),
        (GUJARAT, "Gujarat"),
        (HYDERABAD, "Hyderabad"),
        (THIRD_PARTY, "THIRD_PARTY"),
        (TATPAR, "TATPAR"),
        (RAJASTHAN, "RAJASTHAN")
    )

    USER = 0
    EXTERNAL = 1
    API = 2

    PAYMENT_SOURCE_CHOICE = (
        (USER, "User"),
        (EXTERNAL, "External"),
        (API, "API"),
    )

    pdf_url = models.CharField(max_length=255, null=True, blank=True)
    under_investigation = models.BooleanField(default=False)
    # image_url_list = JSONField(null=True, blank=True)
    challan_no = models.CharField(max_length=255, null=True, blank=True, db_index=True, unique=True)
    challan_datetime = models.CharField(max_length=255, null=True, blank=True)
    lat_long = models.CharField(max_length=255, null=True, blank=True)  #
    officer_id = models.PositiveIntegerField(null=True, blank=True)
    accused_name = models.CharField(max_length=255, null=True, blank=True)
    accused_father_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    challan_address = models.CharField(max_length=255, null=True, blank=True)
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    chassis_number = models.CharField(max_length=255, null=True, blank=True)
    vehicle_class = models.CharField(max_length=255, null=True, blank=True)
    challan_status = models.CharField(max_length=255, null=True, blank=True)
    payment_date = models.CharField(max_length=255, null=True, blank=True)
    document_number = models.CharField(max_length=255, null=True, blank=True)
    payment_source = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=255, null=True, blank=True)
    sent_to_court_on = models.CharField(max_length=255, null=True, blank=True)
    court_name = models.CharField(max_length=255, blank=True, null=True)
    court_address = models.CharField(max_length=255, blank=True, null=True)
    traffic_police = models.PositiveIntegerField(null=True, blank=True)
    challan_source = models.PositiveIntegerField(null=True, blank=True)
    for_online_payment_ch = models.PositiveIntegerField(null=True, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    court_status = models.CharField(max_length=255, null=True, blank=True)
    vehicle_impound = models.CharField(max_length=255, null=True, blank=True)
    state_code = models.CharField(max_length=255, null=True, blank=True)
    payment_eligible = models.PositiveIntegerField(null=True, blank=True)
    vehicle_number = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    data_source = models.PositiveIntegerField(choices=CHALLAN_DATA_SOURCE, null=True, blank=True)
    payment_source_of_truth = models.PositiveIntegerField(
        choices=PAYMENT_SOURCE_CHOICE, null=True, blank=True
    )  # payment paid status updated by whom
    payment_verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "challan_detail"


class ChallanOffenceDetails(models.Model):
    challan_id = models.PositiveIntegerField(db_index=True)
    offence_id = models.PositiveIntegerField(null=True, blank=True)
    offence_name = models.TextField(null=True, blank=True)
    mva = models.CharField(max_length=255, null=True, blank=True)
    mva1 = models.CharField(max_length=255, null=True, blank=True)
    penalty = models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "challan_offence_detail"


class BrandMapping(models.Model):
    brand_string = models.CharField(max_length=255, db_index=True)
    brand_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "brand_mapping"


class VehicleServiceFeedback(models.Model):
    CHALLAN = 1
    SEARCH_VEHICLE = 2

    SERVICE_TYPES = ((CHALLAN, "Challan"), (SEARCH_VEHICLE, "SearchVehicle"))

    user_id = models.PositiveIntegerField(db_index=True)
    license = models.CharField(max_length=255)
    service_type = models.PositiveIntegerField(choices=SERVICE_TYPES, null=True, blank=True)
    is_service_helpful = models.BooleanField(null=True)
    service_feedback = models.TextField(null=True, blank=True)
    # feedback_values = JSONField(null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "vehicle_service_feedback"


class UserChallanSearchData(CommonModel):
    user_id = models.PositiveIntegerField(db_index=True)
    license = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "user_challan_search_data"
        unique_together = ("user_id", "license")


class AuditLog(models.Model):
    CREATED = "created"
    UPDATED = "updated"
    SOFT_DELETED = "soft_deleted"
    EVENT_TYPE = ((CREATED, "Created"), (UPDATED, "Updated"), (SOFT_DELETED, "Deleted"))
    API = "api"
    DASHBOARD = "dashboard"
    B2C_APP = "b2c_app"
    OP_APP = "op_app"
    COMMAND = "command"
    ADMIN_DASHBOARD = "admin_dashboard"
    REQUEST_SOURCE = (
        (API, "API"),
        (DASHBOARD, "DASHBOARD"),
        (B2C_APP, "B2C_APP"),
        (OP_APP, "OP_APP"),
        (ADMIN_DASHBOARD, "ADMIN_DASHBOARD"),
        (COMMAND, "COMMAND"),
    )
    updated_by_user_id = models.PositiveIntegerField(null=True)
    model_name = models.CharField(max_length=64, null=True, blank=True)
    row_id = models.PositiveIntegerField(null=True)
    # old_data = JSONField(null=True)
    # new_data = JSONField(null=True)
    event_type = models.CharField(max_length=255, choices=EVENT_TYPE)
    source = models.CharField(max_length=255, choices=REQUEST_SOURCE)
    end_point = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "audit_log"


class CarMake(CommonModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "car_make"


def year_choices():
    return [(r, r) for r in range(1900, datetime.today().year + 1)]


class CarModel(CommonModel):
    BODY_TYPE_CONVERTIBLE = "Convertible"
    BODY_TYPE_COUPE = "Coupe"
    BODY_TYPE_MPV = "MPV"
    BODY_TYPE_SEDAN = "Sedan"
    BODY_TYPE_HATCHBACK = "Hatchback"
    BODY_TYPE_CROSSOVER = "Crossover"
    BODY_TYPE_LIFEBACK = "Lifeback"
    BODY_TYPE_PICKUP = "Pickup"
    BODY_TYPE_SUV = "SUV"
    BODY_TYPE_TARGA = "Targa"
    BODY_TYPE_WAGON = "Wagon"
    BODY_TYPE_CHOICES = (
        ("Convertible", BODY_TYPE_CONVERTIBLE),
        ("Coupe", BODY_TYPE_COUPE),
        ("MPV", BODY_TYPE_MPV),
        ("Sedan", BODY_TYPE_SEDAN),
        ("Hatchback", BODY_TYPE_HATCHBACK),
        ("Crossover", BODY_TYPE_CROSSOVER),
        ("Lifeback", BODY_TYPE_LIFEBACK),
        ("Pickup", BODY_TYPE_PICKUP),
        ("SUV", BODY_TYPE_SUV),
        ("Targa", BODY_TYPE_TARGA),
        ("Wagon", BODY_TYPE_WAGON),
    )
    name = models.CharField(max_length=255)
    body_type = models.CharField(max_length=255, choices=BODY_TYPE_CHOICES)
    cw_body_type = models.CharField(max_length=255, null=True, help_text="Car wash body type")
    make = models.ForeignKey(CarMake, on_delete=models.PROTECT)
    year_start = models.IntegerField(choices=year_choices(), null=True, blank=True)
    year_end = models.IntegerField(choices=year_choices(), null=True, blank=True)
    wheel_count = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = ["name", "make", "year_start", "year_end", ]
        db_table = "car_model"


class Variant(CommonModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    year_start = models.IntegerField(choices=year_choices(), null=True, blank=True)
    year_end = models.IntegerField(choices=year_choices(), null=True, blank=True)
    is_discontinued = models.BooleanField(default=False)
    image_urls = models.TextField(null=True, blank=True)
    # extra_data = JSONField(null=True, blank=True)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    wheel_count = models.PositiveIntegerField(null=True)

    class Meta:
        unique_together = [
            "name",
            "car_model",
            "year_start",
            "year_end",
        ]
        db_table = "car_variant"


class VariantPropertyCategory(CommonModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    wheel_count = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = "car_variant_property_category"


class VariantPropertyType(CommonModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(VariantPropertyCategory, on_delete=models.PROTECT)
    code = models.CharField(max_length=255, unique=True)
    wheel_count = models.PositiveIntegerField(null=True)

    class Meta:
        db_table = "car_variant_property_type"


class VariantPropertyValue(CommonModel):
    type = models.ForeignKey(VariantPropertyType, on_delete=models.PROTECT)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        unique_together = ["type", "variant", ]
        db_table = "car_variant_property_value"


class CarDekhoVariantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class CarDekhoVariant(CommonModel):
    mid_make = models.PositiveIntegerField(null=True, blank=True)
    mid_model = models.PositiveIntegerField(null=True, blank=True)
    mid_variant_id = models.PositiveIntegerField(null=True, blank=True)
    manufacturer_id = models.PositiveIntegerField(null=True, blank=True)
    manufacturer_model_id = models.PositiveIntegerField(null=True, blank=True)
    variant_id = models.PositiveIntegerField(db_index=True)
    make_name = models.CharField(max_length=255, db_index=True)
    model_name = models.CharField(max_length=255, db_index=True)
    variant_name = models.CharField(max_length=255, db_index=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    active = models.BooleanField(default=False)
    objects = CarDekhoVariantManager()


class CarDekhoCity(CommonModel):
    city_id = models.PositiveIntegerField()
    mid_city_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    available = models.BooleanField()
    location = PointField(srid=4326, null=True, blank=True)
    state_id = models.PositiveIntegerField(null=True, blank=True)
    state_mid_id = models.PositiveIntegerField(null=True, blank=True)
    store_id = models.PositiveIntegerField(null=True, blank=True)
    is_hi = models.BooleanField()
    remove_internal_bidding_status = models.BooleanField()

    class Meta:
        ordering = ['name']


class CarDekhoPricingMap(CommonModel):
    city = models.ForeignKey('CarDekhoCity', on_delete=models.CASCADE)
    variant = models.ForeignKey('CarDekhoVariant', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', related_name='car_dekho_pricing', on_delete=models.CASCADE)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1984), MaxValueValidator(datetime.now().year)])
    # pricing = JSONField()

    class Meta:
        ordering = ['-created']


class CarDekhoBooking(CommonModel):
    BOOKING_INITIATED = "INITIATED"  # Default value while adding entry
    BOOKING_QUEUED = "QUEUED"  # When attempt to send booking to cardekho is started
    BOOKING_SUCCESS = "SUCCESS"  # When cardekho has successfully consumed the data
    BOOKING_FAILED = "FAILED"  # When cardekho has successfully consumed the data
    BOOKING_CHOICES = (
        (BOOKING_INITIATED, BOOKING_INITIATED),
        (BOOKING_QUEUED, BOOKING_QUEUED),
        (BOOKING_SUCCESS, BOOKING_SUCCESS),
        (BOOKING_FAILED, BOOKING_FAILED),
    )
    user_id = models.PositiveIntegerField()
    vehicle = models.ForeignKey('Vehicle', related_name='car_dekho_bookings', on_delete=models.PROTECT)
    car_dekho_pricing_map = models.ForeignKey('CarDekhoPricingMap', related_name='car_dekho_bookings',
                                              on_delete=models.PROTECT, null=True, blank=True)
    # extra_data = JSONField()
    cardekho_booking_status = models.CharField(max_length=255, choices=BOOKING_CHOICES, default=BOOKING_INITIATED)


class PassTemplate(CommonModel):
    CAR = 4
    BIKE = 2
    TRUCK = 6
    EIGHT_WHEELER = 8
    TEN_WHEELER = 10

    WHEEL_COUNT = ((CAR, "car"), (BIKE, "bike"), (TRUCK, "truck"),
                   (EIGHT_WHEELER, "eight wheeler"), (TEN_WHEELER, "ten wheeler"))

    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    QUARTERLY = 4
    UNLIMITED = 5
    OTHERS = 6

    PASS_TYPES = ((DAILY, "daily"), (WEEKLY, "weekly"), (MONTHLY, "monthly"),
                  (QUARTERLY, "quarterly"), (UNLIMITED, "unlimited"),(OTHERS,"others"))

    project_id = models.IntegerField()
    company_id = models.IntegerField(null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200)
    is_enabled = models.BooleanField(default=True)
    amount = models.IntegerField(validators=[MaxValueValidator(10000000)])
    wheel_count = models.IntegerField()
    pass_type = models.IntegerField(choices=PASS_TYPES)
    activation_date = models.DateField()
    valid_from = models.TimeField(null=True, blank=True)
    valid_till = models.TimeField(null=True, blank=True)
    mobile_number_mandatory = models.BooleanField(default=False)
    charges = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=True)
    re_print = models.BooleanField(default=True)
    duration = models.IntegerField(null=True, blank=True)
    expire_at_midnight = models.BooleanField(default=True)
    calculate_overstay = models.BooleanField(default=False)

    class Meta:
        db_table = "pass_template"


class NonParkplusTag(CommonModel):
    TYPES = {
        'FASTAG': 1,
        'OTHER': 2,
    }
    project_id = models.IntegerField(db_index=True)
    parkplus_tag_id = models.CharField(max_length=100, null=True)
    gate_id = models.IntegerField(null=True)
    device_id = models.IntegerField(null=True)
    type = models.IntegerField(null=True)
    event_time = models.DateTimeField(null=True)
    event_type = models.CharField(max_length=100, null=True)
    non_parkplus_tag_id = models.CharField(max_length=100)


class SuperTag(CommonModel):

    TAG_STATUS_PENDING = "Pending"
    TAG_STATUS_QUEUED = "Queued"
    TAG_STATUS_CREATED = "Created"
    TAG_STATUS_FAILED = "Failed"
    TAG_STATUS_CANCELLED = "Cancelled"
    TAG_STATUS_INVALID_TAG = "Invalid_Tag"
    TAG_STATUS_VEHICLE_ALREADY_REGISTERED = "Vehicle_Already_Registered"
    TAG_STATUS_KYC_LIMIT_EXCEEDED = "KYC_Limit_Exceeded"
    TAG_STATUS_INVALID_REQUEST = "Invalid_Request_Parameter"
    TAG_STATUS_VEHICLE_BLACKLISTED = "Vehicle_Blacklisted"
    TAG_STATUS_VIRTUAL_ACCOUNT_NO_BALANCE = "Virtual_Account_No_Balance"


    PAYMENT_MODES = (("CASH", "Cash"),)
    PAYMENT_STATUS_COLLECTED = "COLLECTED"
    PAYMENT_STATUS_INITIATED = "INITIATED"
    PAYMENT_STATUS = (
        (PAYMENT_STATUS_INITIATED, PAYMENT_STATUS_INITIATED),
        (PAYMENT_STATUS_COLLECTED, PAYMENT_STATUS_COLLECTED),
    )
    ACQUIRERS = (("IDFC", "Idfc"),("IDBI","Idbi"))

    TAG_STATUS = (
        (TAG_STATUS_PENDING, TAG_STATUS_PENDING),
        (TAG_STATUS_QUEUED, TAG_STATUS_QUEUED),
        (TAG_STATUS_CREATED, TAG_STATUS_CREATED),
        (TAG_STATUS_FAILED, TAG_STATUS_FAILED),
        (TAG_STATUS_CANCELLED,TAG_STATUS_CANCELLED),
        (TAG_STATUS_INVALID_TAG,TAG_STATUS_INVALID_TAG),
        (TAG_STATUS_VEHICLE_ALREADY_REGISTERED,TAG_STATUS_VEHICLE_ALREADY_REGISTERED),
        (TAG_STATUS_KYC_LIMIT_EXCEEDED,TAG_STATUS_KYC_LIMIT_EXCEEDED)
    )

    SOURCE_TOA = "toa"
    SOURCE_B2C = "b2c"
    SOURCE_DEALER = "dealer"
    SOURCE_CHOICES = (
        (SOURCE_TOA, SOURCE_TOA),
        (SOURCE_B2C, SOURCE_B2C),
        (SOURCE_DEALER, SOURCE_DEALER)
    )

    CUSTOMER_ACTIVATION_PENDING = "PENDING"
    CUSTOMER_ACTIVATION_SUCCESS = "SUCCESS"
    CUSTOMER_ACTIVATION_TIME_OUT = "TIME_OUT"

    CUSTOMER_ACTIVATION_STATUS = (
        (CUSTOMER_ACTIVATION_PENDING, CUSTOMER_ACTIVATION_PENDING),
        (CUSTOMER_ACTIVATION_SUCCESS, CUSTOMER_ACTIVATION_SUCCESS),
        (CUSTOMER_ACTIVATION_TIME_OUT, CUSTOMER_ACTIVATION_TIME_OUT)
    )

    vehicle_id = models.PositiveIntegerField()
    project_id = models.PositiveIntegerField(null=True, blank=True)
    operator_id = models.PositiveIntegerField(null=True, blank=True)
    order_id = models.PositiveIntegerField(null=True, blank=True)
    tag_id = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default=SOURCE_TOA)
    payment_mode = models.CharField(max_length=255, choices=PAYMENT_MODES, null=True, blank=True)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=255, choices=PAYMENT_STATUS, default=PAYMENT_STATUS_INITIATED)
    qr_code = models.CharField(max_length=255, null=True, blank=True)
    third_party_customer_id = models.PositiveIntegerField(null=True)
    acquirer = models.CharField(max_length=255, choices=ACQUIRERS, default=ACQUIRERS[0][0])
    tag_status = models.CharField(max_length=255, choices=TAG_STATUS, default=TAG_STATUS[0][0])
    remark =  models.CharField(max_length=255, null=True, blank=True)
    # extra_data = JSONField(null=True, blank=True)
    tag_issue_date = models.DateTimeField(null=True, blank=True)
    issue_tag_retry = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(null=True,blank=True)
    parent_supertag_id = models.PositiveIntegerField(null=True, blank=True)
    dealer_id = models.PositiveIntegerField(null=True, blank=True)
    fitment_certificate_link = models.CharField(max_length=255, null=True, blank=True)
    chassis = models.CharField(max_length=255, null=True, blank=True)
    customer_activation_status = models.CharField(max_length=255, choices=CUSTOMER_ACTIVATION_STATUS, blank=True, null=True)

    # history = HistoricalRecords(excluded_fields=['created', 'vehicle_id', 'project_id', 'operator_id', 'payment_mode', 'amount', 'qr_code',
    #                                              'third_party_customer_id', 'acquirer',"remark"], table_name='super_tag_history')

    class Meta:
        db_table = "super_tag_new"


class CustomerActivationRequestLogs(models.Model):
    CUSTOMER_ACTIVATION_REQUEST_SENT = "SENT"
    CUSTOMER_ACTIVATION_REQUEST_ACCEPTED = "ACCEPTED"

    CUSTOMER_ACTIVATION_STATUS = (
        (CUSTOMER_ACTIVATION_REQUEST_SENT, CUSTOMER_ACTIVATION_REQUEST_SENT),
        (CUSTOMER_ACTIVATION_REQUEST_ACCEPTED, CUSTOMER_ACTIVATION_REQUEST_ACCEPTED)
    )

    super_tag_id = models.PositiveIntegerField(null=True, blank=True)
    user_id = models.PositiveIntegerField(null=True, blank=True)
    operator_id = models.PositiveIntegerField(null=True, blank=True)
    vehicle_id = models.PositiveIntegerField(null=True, blank=True)
    request_status = models.CharField(max_length=255, choices=CUSTOMER_ACTIVATION_STATUS, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "customer_activation_request_logs"


class RequestLogs(CommonModel):
    METHOD_POST = "POST"
    METHOD_GET = "GET"
    METHOD_PUT = "PUT"
    METHOD_CHOICES = (
        (METHOD_POST, METHOD_POST),
        (METHOD_GET, METHOD_GET),
        (METHOD_PUT, METHOD_PUT),
    )
    PARTNER_SIGNZY = "signzy"
    PARTNER_SUREPASS ="surepass"
    PARTNER_CHOICES = (
        (PARTNER_SIGNZY, PARTNER_SIGNZY),
        (PARTNER_SUREPASS,PARTNER_SUREPASS)
    )
    url = models.URLField()
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    partner = models.CharField(max_length=50, choices=PARTNER_CHOICES, )
    unique_key = models.CharField(max_length=255)
    # request_payload = JSONField(null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)
    response_status_code = models.IntegerField(null=True, blank=True)
    request_user_id = models.PositiveIntegerField(null=True)
    request_source = models.CharField(max_length=255, null=True)
    # dump = JSONField(default=[])

    #class Meta:
        #unique_together = ("unique_key", "response_status_code")


class FailedChallan(CommonModel):
    license = models.CharField(max_length=255, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    source_api = models.CharField(max_length=255, null=True, blank=True)
    status_code = models.CharField(max_length=255, null=True, blank=True)
    is_fetched_successfully = models.BooleanField(default=False)

    class Meta:
        db_table = 'failed_challan'


class APITracking(models.Model):
    POST = "Post"
    GET = "Get"
    PATCH = "Patch"
    DELETE = "Delete"

    REQUEST_METHODS = (
        (POST, "Post"),
        (GET, "Get"),
        (PATCH, "Patch"),
        (DELETE, "Delete")
    )

    request_url = models.CharField(max_length=255)
    response_status_code = models.PositiveIntegerField(null=True)
    # request_payload = JSONField(null=True)
    request_method = models.CharField(max_length=255, choices=REQUEST_METHODS, default=REQUEST_METHODS[0][0])
    response_data = models.TextField(null=True)
    # headers = JSONField(null=True)
    response_time = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class VehicleEPCMapping(CommonModel):
    project_id = models.PositiveIntegerField(null=True, blank=True)
    license = models.CharField(max_length=255, null=True, blank=True)
    epc_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'vehicle_epc_mapping'


class BlacklistTag(CommonModel):
    PARKWHEELS = 0
    OTHERS = 1
    PARKPLUS = 2
    NONPARKPLUS = 3
    IDFC_FASTAG = 4
    TAG_SOURCE = (
        (PARKWHEELS, "Parkwheels"),
        (OTHERS, "Others"),
        (PARKPLUS, "Parkplus"),
        (NONPARKPLUS, "Non Parkplus"),
        (IDFC_FASTAG, "IDFC Fastag"),
    )

    NFC = 0
    RFID = 1

    TAG_TYPES = ((NFC, "nfc"), (RFID, "rfid"))

    HANDHELD = 0
    WINDSHIELD = 1

    TAG_CATEGORY = ((HANDHELD, "Handheld"), (WINDSHIELD, "Windshield"))

    MANUAL_ASSIGNMENT = 0
    MONOLITHIC = 1
    TAG_ONBOARDING = 2

    ASSIGNMENT_SOURCES = (
        (MANUAL_ASSIGNMENT, "Manual Assignment"),
        (MONOLITHIC, "Monolithic"),
        (TAG_ONBOARDING, "TagOnboarding"),
    )

    tag_id = models.CharField(max_length=255, null=True, blank=True, db_index=True, unique=True)
    tag_id2 = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    np_tag_id = models.CharField(max_length=255, null=True, blank=True, db_index=True)  # non parkplus tag_id
    tag_secret_code = models.CharField(max_length=255, null=True, blank=True)
    tag_category = models.PositiveIntegerField(choices=TAG_CATEGORY, null=True, blank=True)
    source = models.PositiveIntegerField(choices=TAG_SOURCE, null=True)
    tid = models.CharField(max_length=255, null=True, blank=True)
    tag_type = models.PositiveIntegerField(choices=TAG_TYPES, null=True)
    # meta_data = JSONField(default={}, blank=True, null=True)
    epc_code = models.CharField(max_length=255, null=True, blank=True)
    tag_id_md5 = models.CharField(max_length=64, null=True, blank=True)
    tag_id2_md5 = models.CharField(max_length=64, null=True, blank=True)
    secret_code_md5 = models.CharField(max_length=64, null=True, blank=True)
    assignment_source = models.PositiveIntegerField(choices=ASSIGNMENT_SOURCES, null=True, blank=True)
    partner_enabled = models.BooleanField(default=False)
    partner_name = models.CharField(max_length=255, null=True, blank=True)
    is_supertag = models.BooleanField(default=False)
    bar_code = models.CharField(max_length=255, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    blacklist_by = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "blacklist_tags"

    def get_tag_source(self):
        tag_source_dict = dict(self.TAG_SOURCE)
        return tag_source_dict[self.source] if self.source else None

    def get_tag_type(self):
        tag_type_dict = dict(self.TAG_TYPES)
        return tag_type_dict[self.tag_type] if self.tag_type else None


class TollTransactionRequest(CommonModel):
    request_id = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    response_code = models.CharField(max_length=100, null=True, blank=True)
    response_msg = models.CharField(max_length=255, null=True, blank=True)
    entity_id = models.IntegerField(null=True, blank=True)
    from_date = models.DateTimeField(null=True, blank=True)
    to_date = models.DateTimeField(null=True, blank=True)
    transaction_count = models.IntegerField(null=True, blank=True)
    response_data = models.TextField(null=True, blank=True)
    xml_request = models.TextField(null=True, blank=True)
    class Meta:
        db_table = "toll_transaction_request"


class TollTransaction(CommonModel):

    REASON_CODES_DA = (('452', "CREDIT CHARGEBACK ACCEPTANCE"),
                       ('502', "CREDIT CHARGEBACK DEEMED ACCEPTANCE'"),
                       ('474', "PRE-ARBITRATION ACCEPTANCE"),
                       ('480', "ARBITRATION ACCEPTANCE"),
                       ('700', "MEMBER FUND COLLECTION"),
                       ('760', "NPCI FEE COLLECTION"),
                       ('681', "GOOD FAITH RAISE ACCEPTANCE"),
                       ('673', "PRE-COMPLIANCE ACCEPTANCE"),
                       ('763', "DEBIT ADJUSTMENT"))

    toll_request_id = models.IntegerField(null=True, blank=True)
    client_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    tag_id = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    processing_date = models.DateTimeField(null=True, blank=True)
    transaction_number = models.CharField(max_length=255, null=True, blank=True)
    plaza_id = models.CharField(max_length=255, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    transaction_type = models.CharField(max_length=2, null=True, blank=True)
    credit_amount = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)
    debit_amount = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)
    balance_amount = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)
    transaction_details = models.CharField(max_length=255, null=True, blank=True)
    post_transaction_balance = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)
    transaction_processing_time = models.DateTimeField(null=True, blank=True)
    recharge_amount = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)  # amount in paisa
    available_balance = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)
    original_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    reason_code_debit_adjustment = models.CharField(max_length=100, choices=REASON_CODES_DA,  null=True, blank=True)
    lane_direction = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        db_table = "toll_transaction"


class MoengageNotificationLogs(models.Model):

    INSURANCE = 0
    PUCC = 1

    USER = "User"
    SIGNZY = "Signzy"

    REMINDER_TYPE = ((INSURANCE, "Insurance"), (PUCC, "PUCC"))
    SOURCES = ((USER, "User"), (SIGNZY, "Signzy"))

    reminder_date = models.DateField(null=True, blank=True)
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    user_id=models.PositiveIntegerField(null=True, blank=True, db_index=True)
    event_time=models.CharField(max_length=255, null=True, blank=True)
    vehicle_id=models.PositiveIntegerField(null=True, blank=True, db_index=True)
    reminder_type = models.PositiveIntegerField(null=True, blank=True, choices=REMINDER_TYPE)
    source = models.CharField(max_length=255, choices=SOURCES, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "moengage_notification_logs"


class PartnerAPITracking(models.Model):
    POST = "Post"
    GET = "Get"
    PATCH = "Patch"
    DELETE = "Delete"

    REQUEST_METHODS = (
        (POST, "Post"),
        (GET, "Get"),
        (PATCH, "Patch"),
        (DELETE, "Delete")
    )
    request_url = models.CharField(max_length=255)
    headers = models.TextField(null=True)
    # request_payload = JSONField(null=True)
    request_method = models.CharField(max_length=255, choices=REQUEST_METHODS, default=REQUEST_METHODS[0][0])
    request_time = models.DateTimeField(null=True)
    response_time = models.DateTimeField(null=True)
    response_data = models.TextField(null=True)
    response_status_code = models.PositiveIntegerField(null=True)
    vehicle_number = models.CharField(max_length=255, null=True, blank=True)
    request_id = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "partner_api_tracking"


class KafkaDataLog(models.Model):
    topic_name = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True)
    future_meta_data = models.TextField(null=True)
    is_done = models.BooleanField(null=True)
    exception = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kafka_data_log'


class TagActivationCashback(models.Model):


    order_id = models.CharField(max_length=255, null=True, blank=True,db_index=True)
    user_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    is_cashback_credited = models.BooleanField(default=False)
    amount = models.IntegerField(null=True, blank=True)
    # cahback_response_data = JSONField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "tag_activation_cashback"


class InsuranceDekhoVariant(models.Model):

    make_id = models.PositiveIntegerField(null=True, blank=True)
    model_id = models.PositiveIntegerField(null=True, blank=True)
    version_id = models.PositiveIntegerField(null=True, blank=True)
    make_name = models.CharField(max_length=255,null=True,blank=True)
    model_name = models.CharField(max_length=255, null =True,blank=True)
    version_name = models.CharField(max_length=255,null =True,blank=True)
    seats = models.PositiveIntegerField(null=True, blank=True)
    cc = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.CharField(max_length=255, null=True, blank=True)
    transmission_type = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


    class Meta:
        db_table = "insurance_dekho_variant"


class FastagEPCBlacklistedTags(models.Model):
    
    IDFC_FASTAG = 0
    IDBI_FASTAG = 1
    TAG_SOURCE = (
        (IDFC_FASTAG, "IDFC Fastag"),
        (IDBI_FASTAG, "IDBI Fastag")
    )
    epc_code = models.CharField(max_length=255, null=True, blank=True)
    source = models.PositiveIntegerField(choices=TAG_SOURCE, null=True)
    bar_code =  models.CharField(max_length=255, null=True, blank=True)
    txn_amount = models.CharField(max_length=255, null=True, blank=True)
    txn_date =   models.DateTimeField(null=True, blank=True)
    txn_no = models.CharField(max_length=255, null=True, blank=True)
    # meta_data = JSONField(default={}, blank=True, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "fastag_epc_blacklist_tags"


class ShipTag(models.Model):
    MANUAL_ASSIGNMENT = 0
    MONOLITHIC = 1
    DASHBOARD = 2

    ASSIGNMENT_SOURCES = (
        (MANUAL_ASSIGNMENT, "Manual Assignment"),
        (MONOLITHIC, "Monolithic"),
        (DASHBOARD, "dashboard"),

    )
    epc_code = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    request_id = models.IntegerField(db_index=True, null=True, blank=True)
    assignment_source = models.PositiveIntegerField(choices=ASSIGNMENT_SOURCES, null=True, blank=True)
    bar_code = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "ship_tag"


class ShipTagRequest(models.Model):
    UPLOADED = "UPLOADED"
    FAILED = "FAILED"
    PROCESSING = "PROCESSING"
    
    UPLOAD_STATUS = (
        (PROCESSING, PROCESSING),
        (UPLOADED, UPLOADED),
        (FAILED, FAILED)
    )

    mrf_id = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    added_by = models.CharField(max_length=255, null=True, blank=True)
    fastag_bank = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    courier_name = models.CharField(max_length=64, null=True, blank=True)
    courier_status = models.CharField(max_length=64, null=True, blank=True)
    courier_platform = models.CharField(max_length=64, null=True, blank=True)
    upload_status = models.CharField(max_length=25, choices=UPLOAD_STATUS, default=PROCESSING, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "ship_tag_request"


class FailedShipTag(models.Model):
    MANUAL_ASSIGNMENT = 0
    MONOLITHIC = 1
    DASHBOARD = 2
    



    ASSIGNMENT_SOURCES = (
        (MANUAL_ASSIGNMENT, "Manual Assignment"),
        (MONOLITHIC, "Monolithic"),
        (DASHBOARD, "dashbored"),
    )

    ACTIVATED = "ACTIVATED"
    BLACKLIST = "BLACKLIST"
    NOT_FOUND = "NOT_FOUND"
    ALREADY_UPLOADED = 'ALREADY_UPLOADED'
    STATUS = (
        (ACTIVATED, ACTIVATED),
        (BLACKLIST, BLACKLIST),
        (NOT_FOUND, NOT_FOUND),
        (ALREADY_UPLOADED,ALREADY_UPLOADED)
    )

    request_id = models.IntegerField(db_index=True, null=True, blank=True)
    assignment_source = models.PositiveIntegerField(choices=ASSIGNMENT_SOURCES, null=True, blank=True)
    bar_code = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS, null=True, blank=True)
    remark = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "failed_ship_tag"