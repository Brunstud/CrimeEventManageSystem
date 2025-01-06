from django.db import models
from rest_framework import serializers
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import transaction
from .models import (
    UserProfile, ActionLog,
    CrimeEvent, CrimeType, Resident, Block, Police, Weapon,
    CaseProgress, Clue, Certification, 
    CrimeEventType, CrimeEventPerson, CrimeEventPolice, CrimeEventWeap
)

# UserProfile 序列化器
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['fullname', 'contact', 'email', 'address', 'role']

# 用户认证序列化器
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

# 犯罪事件序列化器
class CrimeEventSerializer(serializers.ModelSerializer):
    # 提取犯罪类型名称
    main_type_name = serializers.CharField(source='main_type.type_name', read_only=True)
    # 提取罪犯名称
    main_criminal_name = serializers.CharField(source='main_criminal.last_name', read_only=True)
    # 提取受害人名称
    main_victim_name = serializers.CharField(source='main_victim.last_name', read_only=True)
    # 提取武器名称
    main_weapon_name = serializers.CharField(source='main_weapon.weapon_description', read_only=True)
    # 提取区块名
    block_name = serializers.CharField(source='block.block_name', read_only=True)
    class Meta:
        model = CrimeEvent
        fields = [
            'id', 'crime_description', 'main_type_name', 'main_criminal_name', 'main_victim_name',
            'main_weapon_name', 'time_occurred', 'block_name', 'current_status'
        ]

# 犯罪事件详细信息序列化器
class CrimeEventDetailSerializer(serializers.ModelSerializer):
    block_name = serializers.CharField(source='block.block_name')
    block_description = serializers.CharField(source='block.domain_description')
    time_reported = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    time_occurred = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    # 获取犯罪类型的详细信息
    types = serializers.SerializerMethodField()
    
    # 获取相关人员
    persons = serializers.SerializerMethodField()
    
    # 获取所有武器信息
    weapons = serializers.SerializerMethodField()
    
    # 获取警官信息
    officers = serializers.SerializerMethodField()

    class Meta:
        model = CrimeEvent
        fields = [
            'crime_description', 'types', 'persons', 'weapons', 'location',
            'latitude', 'longitude', 'block_name', 'block_description', 'time_reported', 'time_occurred',
            'updated_at', 'current_status', 'officers'
        ]

    def get_types(self, obj):
        crime_types = CrimeEventType.objects.filter(event=obj).select_related('type_code')
        return [
            {
                "type_code": ct.type_code.type_code,
                "type_name": ct.type_code.type_name,
                "type_description": ct.type_code.type_description,
                "is_active": ct.type_code.is_active
            }
            for ct in crime_types
        ]

    def get_persons(self, obj):
        persons = CrimeEventPerson.objects.filter(event=obj).select_related('person')
        persons_info = {
            "suspects": [{"name": p.person.first_name + " " + p.person.last_name, "person_id": p.person.person_id} for p in persons if p.relation == 'Susp'],
            "criminals": [{"name": p.person.first_name + " " + p.person.last_name, "person_id": p.person.person_id} for p in persons if p.relation == 'Crim'],
            "victims": [{"name": p.person.first_name + " " + p.person.last_name, "person_id": p.person.person_id} for p in persons if p.relation == 'Vict'],
            "eyewitnesses": [{"name": p.person.first_name + " " + p.person.last_name, "person_id": p.person.person_id} for p in persons if p.relation == 'Eyew'],
            "witnesses": [{"name": p.person.first_name + " " + p.person.last_name, "person_id": p.person.person_id} for p in persons if p.relation == 'Witn'],
        }
        return persons_info

    def get_weapons(self, obj):
        weapons = CrimeEventWeap.objects.filter(event=obj).select_related('weapon')
        return [
            {
                "weapon_code": w.weapon.weapon_code,
                "weapon_description": w.weapon.weapon_description,
                "weapon_detail": w.weapon_detail
            }
            for w in weapons
        ]
        
    def get_officers(self, obj):
        officers = CrimeEventPolice.objects.filter(event=obj).select_related('officer', 'officer__person')
        return [
            {
                "name": f"{o.officer.person.first_name} {o.officer.person.last_name}",
                "rank": o.officer.rank,
                "level": o.level,
                "person_id": o.officer.person.person_id
            }
            for o in officers
        ]

# 犯罪事件创建序列化器
class CrimeEventCreateSerializer(serializers.ModelSerializer):
    types = serializers.ListField(write_only=True, required=False)
    persons = serializers.ListField(write_only=True, required=False)
    weapons = serializers.ListField(write_only=True, required=False)
    
    class Meta:
        model = CrimeEvent
        fields = [
            'crime_description', 'location', 'latitude', 'longitude', 'current_status',
            'time_occurred', 'block', 'types', 'persons', 'weapons'
        ]
    
    def create(self, validated_data):
        # 移除不属于模型的字段
        types_data = validated_data.pop('types', [])
        persons_data = validated_data.pop('persons', [])
        weapons_data = validated_data.pop('weapons', [])
        
        # 添加时间戳
        validated_data['time_reported'] = now()
        validated_data['updated_at'] = now()
        
        # 使用事务确保数据一致性
        with transaction.atomic():
            # 设置主要类型（使用第一个类型作为主类型）
            if types_data:
                type_code = types_data[0].get('type_code')
                type_obj = CrimeType.objects.get(type_code=type_code)
                validated_data['main_type'] = type_obj
            
            # 设置主要武器（使用第一个武器作为主武器）
            if weapons_data:
                weapon_code = weapons_data[0].get('weapon_code')
                weapon_obj = Weapon.objects.get(weapon_code=weapon_code)
                validated_data['main_weapon'] = weapon_obj
            
            # 设置主要罪犯和主要受害者
            main_criminal = None
            main_victim = None
            for p in persons_data:
                person_id = p.get('person_id')
                relation = p.get('relation')
                try:
                    person = Resident.objects.get(person_id=person_id)
                    if relation == 'Crim' and main_criminal is None:
                        main_criminal = person
                    elif relation == 'Vict' and main_victim is None:
                        main_victim = person
                except Resident.DoesNotExist:
                    raise serializers.ValidationError(f"居民ID {person_id} 不存在")
            
            if main_criminal:
                validated_data['main_criminal'] = main_criminal
            if main_victim:
                validated_data['main_victim'] = main_victim
                
            crime_event = super().create(validated_data)
            
            # 处理关联数据
            for t in types_data:
                type_code = t.get('type_code')
                order = t.get('order', 1)  # 如果没有提供 order，默认为 1
                type_obj = CrimeType.objects.get(type_code=type_code)
                CrimeEventType.objects.create(
                    event=crime_event, 
                    type_code=type_obj,
                    order=order  # 添加 order 字段
                )
            
            # 处理相关人员关联表
            for p in persons_data:
                person_id = p.get('person_id')
                relation = p.get('relation')
                try:
                    # 使用 person_id 而不是 id
                    person = Resident.objects.get(person_id=person_id)  # 修改这行
                    CrimeEventPerson.objects.create(event=crime_event, person=person, relation=relation)
                except Resident.DoesNotExist:
                    raise serializers.ValidationError(f"居民ID {person_id} 不存在")

            # 处理武器关联表
            for w in weapons_data:
                weapon_code = w.get('weapon_code')
                weapon_detail = w.get('weapon_detail', '')
                weapon_obj = Weapon.objects.get(weapon_code=weapon_code)
                CrimeEventWeap.objects.create(event=crime_event, weapon=weapon_obj, weapon_detail=weapon_detail)
        return crime_event

# 居民基本信息序列化器
class ResidentListSerializer(serializers.ModelSerializer):
    block = serializers.CharField(source='block.block_name')

    class Meta:
        model = Resident
        fields = ['person_id', 'first_name', 'last_name', 'gender', 'occupation', 'contact', 'block']

# 居民详细信息序列化器
class ResidentDetailSerializer(serializers.ModelSerializer):
    block = serializers.CharField(source='block.block_name')
    block_description = serializers.CharField(source='block.domain_description')

    class Meta:
        model = Resident
        fields = ['person_id', 'first_name', 'last_name', 'gender', 'birthday', 'occupation', 'contact', 'block', 'block_description', 'address']

# 线索列表序列化器
class ClueListSerializer(serializers.ModelSerializer):
    crime_description = serializers.CharField(source='event.crime_description')
    submitted_by = serializers.CharField(source='submitted_by.username')
    event_id = serializers.IntegerField(source='event.id')

    class Meta:
        model = Clue
        fields = ['clue_code', 'event_id', 'crime_description', 'clue_type', 'clue_description', 'submitted_by', 'submitted_at', 'chosen_as_evidence']

# 特定案件线索列表序列化器
class CrimeEventClueListSerializer(serializers.ModelSerializer):
    clue_code = serializers.CharField()
    clue_type = serializers.CharField()
    clue_description = serializers.CharField()
    submitted_by = serializers.CharField(source='submitted_by.username')
    submitted_at = serializers.DateTimeField()

    class Meta:
        model = Clue
        fields = ['clue_code', 'clue_type', 'clue_description', 'submitted_by', 'submitted_at']

# 创建线索序列化器
class ClueCreateSerializer(serializers.ModelSerializer):
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=CrimeEvent.objects.all(),
        source='event'
    )
    
    class Meta:
        model = Clue
        fields = ['event_id', 'clue_type', 'clue_description', 'chosen_as_evidence']

    def create(self, validated_data):
        # 获取最大的 clue_code 值并加1
        max_code = Clue.objects.aggregate(models.Max('clue_code'))['clue_code__max'] or 0
        next_code = max_code + 1
        
        clue = Clue.objects.create(
            clue_code=next_code,  # 使用递增的数字编码
            **validated_data
        )
        
        print(f"ClueCreateSerializer: Created clue with ID {clue.clue_code}")
        return clue

# 案件进展列表序列化器
class CaseProgressListSerializer(serializers.ModelSerializer):
    time_progress = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    
    class Meta:
        model = CaseProgress
        fields = ['progress_code', 'time_progress', 'status', 'notes']

# 更新案件进展的序列化器
class CaseProgressCreateSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CaseProgress
        fields = ['event_id', 'status', 'notes']

    def create(self, validated_data):
        event_id = validated_data.pop('event_id')
        event = CrimeEvent.objects.get(id=event_id)
        
        # 生成进展编码
        progress_code = event_id*1000 + CaseProgress.objects.count() + 1
        
        progress = CaseProgress.objects.create(
            progress_code=progress_code,
            event=event,
            time_progress=now(),
            **validated_data
        )
        
        return progress