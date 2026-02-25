# Django/DRF Coding Rules

## Model Design
- Use UUID as primary key for all models
- Include `created_at` and `updated_at` timestamps
- Use `is_active` boolean for soft delete pattern
- Define `db_table` explicitly in Meta class
- Add database indexes for frequently queried fields

## QuerySet Optimization
- Always use `select_related()` for ForeignKey fields
- Use `prefetch_related()` for reverse relations and ManyToMany
- Avoid N+1 queries - check with Django Debug Toolbar
- Use `only()` or `defer()` for large models when appropriate

## Serializers
- Create separate serializers for list/detail/create/update operations
- Use `SerializerMethodField` for computed properties
- Validate business logic in `validate()` method
- Include `read_only_fields` in Meta class

## Views/ViewSets
- Use ViewSets with custom actions for related operations
- Implement permission classes for role-based access
- Use `get_queryset()` for dynamic filtering
- Return appropriate HTTP status codes

## API Response Format
```python
# 単体オブジェクト
{"id": "...", "area_code": "...", ...}

# リスト（ページネーション）
{"results": [...], "count": 100, "next": "...", "previous": "..."}

# エラー
{"error": "Error message"}
{"detail": "Error details"}
{"field_name": ["Validation error"]}
```

## Security
- Never trust user input - always validate
- Use `get_object_or_404()` with permission checks
- Filter querysets by user's accessible scope
- Check `get_managed_area_ids()` for area-based permissions

## Testing
- Test all ViewSet actions
- Test serializer validation
- Test permission logic
- Use `APITestCase` for API tests
