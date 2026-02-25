# Migration Command

Handle Django database migrations safely with zero-downtime strategies.

## Steps

1. **Check Current Status**
   ```bash
   docker-compose exec backend python manage.py showmigrations
   ```

2. **Create New Migrations**
   ```bash
   docker-compose exec backend python manage.py makemigrations <app_name>
   ```

3. **Review Migration File**
   - Check generated SQL
   - Verify no data loss operations
   - Ensure reversibility

4. **Apply Migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

## Safety Checklist

### Before Migrating
- [ ] Backup database (Supabase dashboard)
- [ ] Review migration files
- [ ] Test on development first
- [ ] Check for destructive operations

### Destructive Operations Warning
These require extra caution:
- `RemoveField`
- `DeleteModel`
- `AlterField` (type changes)
- `RunSQL` with DROP/DELETE

### Rolling Back
```bash
# Rollback to specific migration
docker-compose exec backend python manage.py migrate <app> <migration_number>
```

---

## Zero-Downtime Migration Strategies

### Expand-Contract Pattern（推奨）

大規模な変更を安全に行うための3フェーズアプローチ。

#### Phase 1: EXPAND（後方互換）
```python
# 新列追加（NULL許可、デフォルト値あり）
migrations.AddField(
    model_name='user',
    name='new_email',
    field=models.EmailField(null=True, blank=True),
)
```

#### Phase 2: MIGRATE DATA（バッチ処理）
```python
def migrate_data_in_batches(apps, schema_editor):
    """大量データをバッチ処理で移行"""
    User = apps.get_model('users', 'User')
    batch_size = 1000

    total = User.objects.count()
    for offset in range(0, total, batch_size):
        users = list(User.objects.all()[offset:offset + batch_size])
        for user in users:
            user.new_email = user.email.lower()
        User.objects.bulk_update(users, ['new_email'])

        # 本番環境での負荷軽減
        import time
        time.sleep(0.1)

migrations.RunPython(migrate_data_in_batches, migrations.RunPython.noop)
```

#### Phase 3: CONTRACT（コードデプロイ後）
```python
# NOT NULL制約追加（データ移行完了後）
migrations.AlterField(
    model_name='user',
    name='new_email',
    field=models.EmailField(),
)

# 旧列削除（全コードが新列を使用後）
migrations.RemoveField(
    model_name='user',
    name='old_email',
)
```

### 列名変更の安全な方法

**禁止:** `RenameField` を直接使用

**推奨:** 3段階アプローチ
```python
# Step 1: 新列追加
migrations.AddField('user', 'email_verified', BooleanField(null=True))

# Step 2: データコピー + アプリ更新
# Step 3: 旧列削除（コード移行完了後）
migrations.RemoveField('user', 'is_email_confirmed')
```

### インデックス作成（ロック回避）

大きなテーブルでのインデックス作成：
```python
from django.db import migrations

class Migration(migrations.Migration):
    atomic = False  # トランザクション無効化必須

    operations = [
        migrations.RunSQL(
            sql='CREATE INDEX CONCURRENTLY idx_users_email ON users (LOWER(email));',
            reverse_sql='DROP INDEX IF EXISTS idx_users_email;',
        ),
    ]
```

### NOT NULL追加の安全な方法

```python
# Step 1: デフォルト値付きで列追加
migrations.AddField(
    model_name='store',
    name='base_wage',
    field=models.DecimalField(max_digits=10, decimal_places=2, default=1000),
)

# Step 2: バックフィル
def backfill_wage(apps, schema_editor):
    Store = apps.get_model('organizations', 'Store')
    Store.objects.filter(base_wage__isnull=True).update(base_wage=1000)

migrations.RunPython(backfill_wage, migrations.RunPython.noop)

# Step 3: NOT NULL制約（別マイグレーション推奨）
migrations.AlterField(
    model_name='store',
    name='base_wage',
    field=models.DecimalField(max_digits=10, decimal_places=2),
)
```

---

## 本番データ移行スクリプト例

```python
# apps/users/management/commands/migrate_user_data.py
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = 'Migrate user data safely'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--batch-size', type=int, default=1000)

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        batch_size = options['batch_size']

        from apps.users.models import User

        total = User.objects.count()
        migrated = 0

        for offset in range(0, total, batch_size):
            with transaction.atomic():
                users = User.objects.all()[offset:offset + batch_size]
                for user in users:
                    # 移行ロジック
                    if not dry_run:
                        user.save()
                    migrated += 1

            self.stdout.write(f'Progress: {migrated}/{total}')

        self.stdout.write(self.style.SUCCESS(f'Completed: {migrated} users'))
```

---

## Output Format

```
## Migration Report

### Current State
- Pending migrations: [list]
- Applied migrations: [count]

### Changes Made
1. Migration name
   - Operations: ...
   - Affected models: ...
   - Strategy: [expand-contract / direct / etc.]

### Verification
- [ ] Migrations applied successfully
- [ ] Application running
- [ ] Data integrity verified
- [ ] No locks observed
```
