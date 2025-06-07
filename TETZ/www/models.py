from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departments'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    level = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'positions'
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return f"{self.title} (Level {self.level})"


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class UploadedFile(models.Model):
    FILE_TYPES = (
        ('xml', 'XML'),
        ('xlsx', 'Excel'),
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('mxl', '1C MXL (Комплектация)'),  # Уточненное описание
        ('other', 'Other'),
    )

    file_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255)
    stored_filename = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=50, choices=FILE_TYPES)
    file_size = models.BigIntegerField()  # в байтах
    upload_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        db_table = 'uploaded_files'
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'

    def __str__(self):
        return f"{self.original_filename} ({self.file_type})"


class FileDataMetadata(models.Model):
    DATA_TYPES = (
        ('sales', 'Sales Data'),
        ('inventory', 'Inventory Data'),
        ('customers', 'Customers Data'),
        ('other', 'Other Data'),
    )

    metadata_id = models.AutoField(primary_key=True)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    data_type = models.CharField(max_length=50, choices=DATA_TYPES)
    columns_info = models.JSONField(blank=True, null=True)
    rows_count = models.IntegerField(blank=True, null=True)
    date_range_start = models.DateField(blank=True, null=True)
    date_range_end = models.DateField(blank=True, null=True)
    additional_metadata = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'file_data_metadata'
        verbose_name = 'File Data Metadata'
        verbose_name_plural = 'File Data Metadata'

    def __str__(self):
        return f"Metadata for {self.file.original_filename}"


class Visualization(models.Model):
    VISUALIZATION_TYPES = (
        ('line_chart', 'Line Chart'),
        ('bar_chart', 'Bar Chart'),
        ('pie_chart', 'Pie Chart'),
        ('table', 'Table'),
        ('scatter_plot', 'Scatter Plot'),
        ('heatmap', 'Heatmap'),
        ('other', 'Other'),
    )

    visualization_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    metadata = models.ForeignKey(FileDataMetadata, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    visualization_type = models.CharField(max_length=50, choices=VISUALIZATION_TYPES)
    config = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        db_table = 'visualizations'
        verbose_name = 'Visualization'
        verbose_name_plural = 'Visualizations'

    def __str__(self):
        return f"{self.title} ({self.visualization_type})"


class QueryHistory(models.Model):
    QUERY_TYPES = (
        ('upload', 'File Upload'),
        ('visualize', 'Create Visualization'),
        ('filter', 'Apply Filters'),
        ('export', 'Export Data'),
        ('other', 'Other'),
    )

    query_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_text = models.TextField()
    query_type = models.CharField(max_length=50, choices=QUERY_TYPES)
    execution_time = models.DurationField(blank=True, null=True)
    result_count = models.IntegerField(blank=True, null=True)
    file = models.ForeignKey(UploadedFile, on_delete=models.SET_NULL, blank=True, null=True)
    visualization = models.ForeignKey(Visualization, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    parameters = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'query_history'
        verbose_name = 'Query History'
        verbose_name_plural = 'Query History'

    def __str__(self):
        return f"{self.query_type} by {self.user.username} at {self.timestamp}"


class FavoriteVisualization(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visualization = models.ForeignKey(Visualization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'favorite_visualizations'
        verbose_name = 'Favorite Visualization'
        verbose_name_plural = 'Favorite Visualizations'
        unique_together = ('user', 'visualization')

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.visualization.title}"


class UserActivityLog(models.Model):
    ACTION_TYPES = (
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('file_upload', 'File Upload'),
        ('visualization_create', 'Visualization Created'),
        ('visualization_edit', 'Visualization Edited'),
        ('visualization_delete', 'Visualization Deleted'),
        ('other', 'Other Action'),
    )

    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    action_details = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_activity_logs'
        verbose_name = 'User Activity Log'
        verbose_name_plural = 'User Activity Logs'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.action_type} at {self.timestamp}"

class VisualizationConfig(models.Model):
    config_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    config_data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'visualization_configs'
        verbose_name = 'Visualization Configuration'
        verbose_name_plural = 'Visualization Configurations'
        unique_together = ('user', 'name')

        def __str__(self):
            return f"{self.name} (User: {self.user.username})"


class ImprovementProposal(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'Подано'),
        ('review', 'На рассмотрении'),
        ('approved', 'Утверждено'),
        ('rejected', 'Отклонено'),
        ('implemented', 'Внедрено'),
    ]

    registration_number = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Регистрационный номер")
    submission_date = models.DateField(verbose_name="Дата подачи предложения")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='improvement_proposals',
                               verbose_name="Автор")
    department = models.CharField(max_length=100, verbose_name="Подразделение")
    participation_coefficient = models.PositiveIntegerField(default=100, verbose_name="Коэффициент участия")

    current_situation = models.TextField(verbose_name="Существующая ситуация (проблема)")
    current_situation_sketch = models.FileField(upload_to='ppu/sketches/', blank=True, null=True,
                                                verbose_name="Эскиз текущей ситуации")

    proposed_solution = models.TextField(verbose_name="Предлагаемое решение")
    solution_sketch = models.FileField(upload_to='ppu/sketches/', blank=True, null=True, verbose_name="Эскиз решения")

    expected_result = models.TextField(verbose_name="Ожидаемый результат (эффект)")
    ready_to_implement = models.BooleanField(default=False, verbose_name="Готов внедрить самостоятельно")
    required_resources = models.TextField(blank=True, verbose_name="Необходимые ресурсы")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    document = models.FileField(upload_to='ppu/documents/', blank=True, null=True, verbose_name="Документ ППУ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Предложение по улучшению"
        verbose_name_plural = "Предложения по улучшению"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.registration_number:
            last_proposal = ImprovementProposal.objects.order_by('-id').first()
            last_id = last_proposal.id if last_proposal else 0
            self.registration_number = f"ППУ-{last_id + 1:05d}"

        if not self.submission_date:
            self.submission_date = self.created_at.date()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.registration_number} - {self.author.get_full_name()}"