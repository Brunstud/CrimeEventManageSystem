from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime
from django.db.models import Q, F
from django.db.models.functions import Greatest
from .models import (
    UserProfile, ActionLog,
    CrimeEvent, CrimeType, Resident, Block, Police, Weapon,
    CaseProgress, Clue,
    Certification, CrimeEventType, CrimeEventPerson, CrimeEventPolice, CrimeEventWeap
)
from .serializers import (
    UserProfileSerializer,
    CrimeEventSerializer, CrimeEventDetailSerializer, CrimeEventCreateSerializer,
    ResidentListSerializer, ResidentDetailSerializer,
    ClueListSerializer, CrimeEventClueListSerializer, ClueCreateSerializer,
    CaseProgressListSerializer, CaseProgressCreateSerializer
)
from django.db import transaction

# 用户认证视图
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("LoginView: Received request data:", request.data)
        count = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=count, password=password)
        if user is None:
            user = authenticate(username=count, password=password)
        if user:
            print("LoginView: User authenticated:", user.username)
            token = RefreshToken.for_user(user)
            user_profile = UserProfile.objects.get(user=user)
            data = {
                "token": str(token.access_token),
                "user": UserProfileSerializer(user_profile).data,
            }
            # 记录用户登录日志
            ActionLog.objects.create(user=user, action="User logged in")
            return Response(data, status=200)
        print("LoginView: Authentication failed")
        return Response({"error": "Invalid credentials"}, status=401)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("RegisterView: Received request data:", request.data)
        email = request.data.get("email")
        fullname = request.data.get("fullname")
        password = request.data.get("password")
        contact = request.data.get("contact")
        address = request.data.get("address")
        role = request.data.get("role")
        
        if User.objects.filter(username=email).exists():
            print("RegisterView: User already exists:", email)
            return Response({"error": "User already exists"}, status=400)
        
        user = User.objects.create_user(username=fullname, email=email, password=password)
        user_profile = UserProfile.objects.create(user=user, fullname=fullname, contact=contact, email=email, address=address, role=role)
        
        # 记录注册日志
        ActionLog.objects.create(user=user, action="User registered")
        
        response_data = UserProfileSerializer(user_profile).data
        print("RegisterView: Created user profile:", response_data)
        return Response(response_data, status=201)

class IdentityBindView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        person_id = request.data.get("person_id")
        officer_id = request.data.get("officer_id", None)

        # 更新认证关系
        try:
            person = Resident.objects.get(id=person_id)
            officer = Police.objects.get(id=officer_id) if officer_id else None

            # 创建或更新Certification表
            certification, created = Certification.objects.get_or_create(user=user)
            certification.person = person
            certification.officer = officer
            certification.is_police = officer is not None
            certification.save()

            # 记录身份绑定日志
            ActionLog.objects.create(user=user, action="User identity bound")
            return Response({"success": True, "message": "Identity bound successfully."})
        except Resident.DoesNotExist:
            return Response({"error": "Resident not found"}, status=404)
        except Police.DoesNotExist:
            return Response({"error": "Officer not found"}, status=404)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取当前用户的 UserProfile
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serialized_data = UserProfileSerializer(user_profile).data
            
            # 记录查看用户信息的日志
            ActionLog.objects.create(user=request.user, action="Viewed user profile")
            
            return Response(serialized_data)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=404)

# 犯罪事件视图
class CrimeEventPagination(PageNumberPagination):
    page_size = 10  # 每页显示10条记录
    page_size_query_param = 'page_size'
    max_page_size = 100  # 最大每页显示记录数

class CrimeEventViewSet(viewsets.ModelViewSet):
    queryset = CrimeEvent.objects.all().order_by('-time_reported')
    pagination_class = CrimeEventPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return CrimeEventSerializer
        elif self.action == 'retrieve':
            return CrimeEventDetailSerializer
        elif self.action == 'create':
            return CrimeEventCreateSerializer
    
    def list(self, request, *args, **kwargs):
        """返回犯罪事件表中的基本信息"""
        print(f"CrimeEventViewSet: Received list request from user {request.user.username}")
        
        # 获取搜索关键词
        search_query = request.query_params.get('search', '')
        if search_query:
            self.queryset = self.queryset.filter(
                Q(crime_description__icontains=search_query) |
                Q(block__block_name__icontains=search_query) |
                Q(main_type__type_name__icontains=search_query)
            )
            
        # 记录查看犯罪事件列表的日志
        ActionLog.objects.create(user=request.user, action="Viewed crime event list")
            
        response = super().list(request, *args, **kwargs)
        print(f"CrimeEventViewSet: List response - {response.data}")
        return response

    def retrieve(self, request, *args, **kwargs):
        """返回犯罪事件的详细信息"""
        print(f"CrimeEventViewSet: Retrieving details for CrimeEvent ID {kwargs.get('pk')}")
        
        try:
            crime_event = CrimeEvent.objects.get(pk=kwargs.get('pk'))  # 查询数据库中的犯罪事件
            
            # 记录查看犯罪事件详情的日志
            ActionLog.objects.create(user=request.user, action=f"Viewed crime event detail - ID: {kwargs.get('pk')}")
            
        except CrimeEvent.DoesNotExist:
            return Response({"error": "CrimeEvent not found"}, status=404)  # 如果找不到,返回404响应

        # 使用 CrimeEventDetailSerializer 对犯罪事件进行序列化
        serializer = CrimeEventDetailSerializer(crime_event)
        
        # 输出调试信息
        print(f"CrimeEventViewSet: Retrieve response - {serializer.data}")

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """提交犯罪事件"""
        print(f"CrimeEventViewSet: Received create request with data - {request.data}")
        
        with transaction.atomic():
            # 创建主事件
            serializer = CrimeEventCreateSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            crime_event = serializer.save()
            
            # 记录创建犯罪事件的日志
            ActionLog.objects.create(user=request.user, action=f"Created new crime event - ID: {crime_event.id}")
            
            print(f"CrimeEventViewSet: Created crime event with ID {crime_event.id}")

            return Response({
                'id': crime_event.id,
                'message': '犯罪事件创建成功！'
            })

# 居民视图
class ResidentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resident.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ResidentListSerializer
        elif self.action == 'retrieve':
            return ResidentDetailSerializer

    def list(self, request, *args, **kwargs):
        """返回居民列表"""
        print(f"ResidentViewSet: Received list request from user {request.user.username}")
        
        search_query = request.query_params.get('search', '')
        if search_query:
            self.queryset = self.queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(occupation__icontains=search_query) |
                Q(block__block_name__icontains=search_query)
            )
            
        # 记录查看居民列表的日志
        ActionLog.objects.create(user=request.user, action="Viewed resident list")
        
        response = super().list(request, *args, **kwargs)
        print(f"ResidentViewSet: List response - {response.data}")
        return response

    def retrieve(self, request, *args, **kwargs):
        """返回居民详细信息"""
        print(f"ResidentViewSet: Retrieving details for Resident ID {kwargs.get('pk')}")
        
        # 记录查看居民详情的日志
        ActionLog.objects.create(user=request.user, action=f"Viewed resident detail - ID: {kwargs.get('pk')}")
        
        response = super().retrieve(request, *args, **kwargs)
        print(f"ResidentViewSet: Retrieve response - {response.data}")
        return response

# 线索管理视图
class ClueViewSet(viewsets.ModelViewSet):
    queryset = Clue.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ClueListSerializer
        elif self.action == 'retrieve':
            return CrimeEventClueListSerializer
        elif self.action == 'create':
            return ClueCreateSerializer

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', '')
        if search_query:
            self.queryset = self.queryset.filter(
                Q(clue_description__icontains=search_query) |
                Q(clue_type__icontains=search_query) |
                Q(event__crime_description__icontains=search_query)
            )
            
        # 记录查看线索列表的日志
        ActionLog.objects.create(user=request.user, action="Viewed clue list")
        
        response = super().list(request, *args, **kwargs)
        print(f"ClueViewSet: List response - {response.data}")
        return response
    
    # 获取特定事件的线索列表
    @action(detail=True, methods=['get'])
    def clues_for_event(self, request, pk=None):
        event = CrimeEvent.objects.get(id=pk)
        clues = Clue.objects.filter(event=event)
        
        search_query = request.query_params.get('search', '')
        if search_query:
            clues = clues.filter(
                Q(clue_description__icontains=search_query) |
                Q(clue_type__icontains=search_query)
            )
            
        # 记录查看特定事件线索的日志
        ActionLog.objects.create(user=request.user, action=f"Viewed clues for event - ID: {pk}")
        
        serializer = CrimeEventClueListSerializer(clues, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取特定事件的线索列表"""
        try:
            event = CrimeEvent.objects.get(id=kwargs.get('pk'))
            clues = Clue.objects.filter(event=event)
            
            search_query = request.query_params.get('search', '')
            if search_query:
                clues = clues.filter(
                    Q(clue_description__icontains=search_query) |
                    Q(clue_type__icontains=search_query)
                )
                
            # 记录查看特定事件线索的日志
            ActionLog.objects.create(user=request.user, action=f"Retrieved clues for event - ID: {kwargs.get('pk')}")
            
            serializer = CrimeEventClueListSerializer(clues, many=True)
            response_data = {
                'count': clues.count(),
                'results': serializer.data
            }
            print(f"ClueViewSet: Found {clues.count()} clues for event {event.id}")
            return Response(response_data)
        except CrimeEvent.DoesNotExist:
            return Response({
                'success': False,
                'message': f'找不到ID为{kwargs.get("pk")}的案件'
            }, status=404)

    # 提交新的线索
    def create(self, request, *args, **kwargs):
        print("ClueViewSet: Received create request data:", request.data)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            submitted_by=self.request.user,
            submitted_at=datetime.now()
        )
        # 记录创建线索的日志
        ActionLog.objects.create(
            user=self.request.user, 
            action=f"Created new clue"
        )

# 案件进展视图
class CaseProgressViewSet(viewsets.ModelViewSet):
    queryset = CaseProgress.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return CaseProgressListSerializer
        elif self.action == 'retrieve':
            return CaseProgressListSerializer
        elif self.action == 'create':
            return CaseProgressCreateSerializer
        return CaseProgressListSerializer

    def retrieve(self, request, *args, **kwargs):
        """获取案件进展详情，返回该案件的所有进展记录"""
        print(f"CaseProgressViewSet: Retrieving progress for event {kwargs.get('pk')}")
        try:
            event = CrimeEvent.objects.get(id=kwargs.get('pk'))
            progresses = CaseProgress.objects.filter(event=event).order_by('-time_progress')
            
            search_query = request.query_params.get('search', '')
            if search_query:
                progresses = progresses.filter(
                    Q(notes__icontains=search_query) |
                    Q(status__icontains=search_query)
                )
                
            # 记录查看案件进展的日志
            ActionLog.objects.create(user=request.user, action=f"Retrieved case progress for event - ID: {kwargs.get('pk')}")
            
            serializer = CaseProgressListSerializer(progresses, many=True)
            response_data = {
                'count': progresses.count(),
                'results': serializer.data
            }
            print(f"CaseProgressViewSet: Found {progresses.count()} progress records")
            return Response(response_data)
        except CrimeEvent.DoesNotExist:
            print(f"CaseProgressViewSet: Event {kwargs.get('pk')} not found")
            return Response({
                'success': False,
                'message': f'找不到ID为{kwargs.get("pk")}的案件'
            }, status=404)
    
    @action(detail=True, methods=['get'], url_path='progress')
    def progress_for_event(self, request, pk=None):
        """获取特定案件的进展列表"""
        print(f"CaseProgressViewSet: Fetching progress for event {pk}")
        try:
            event = CrimeEvent.objects.get(id=pk)
            progresses = CaseProgress.objects.filter(event=event).order_by('-created_at')
            
            search_query = request.query_params.get('search', '')
            if search_query:
                progresses = progresses.filter(
                    Q(notes__icontains=search_query) |
                    Q(status__icontains=search_query)
                )
                
            # 记录查看案件进展的日志
            ActionLog.objects.create(user=request.user, action=f"Viewed progress for event - ID: {pk}")
            
            serializer = CaseProgressListSerializer(progresses, many=True)
            response_data = {
                'count': progresses.count(),
                'results': serializer.data
            }
            print(f"CaseProgressViewSet: Found {progresses.count()} progress records")
            return Response(response_data)
        except CrimeEvent.DoesNotExist:
            print(f"CaseProgressViewSet: Event {pk} not found")
            return Response({
                'success': False,
                'message': f'找不到ID为{pk}的案件'
            }, status=404)

    # 更新案件进展
    def create(self, request, *args, **kwargs):
        try:
            event_id = request.data.get('event_id')
            event = CrimeEvent.objects.get(id=event_id)
            
            serializer_data = {
                'event_id': event.id,
                'status': request.data.get('status'),
                'notes': request.data.get('notes')
            }
            print(f"CaseProgressViewSet: Creating progress with data - {serializer_data}")
            
            serializer = CaseProgressCreateSerializer(data=serializer_data)
            
            if serializer.is_valid():
                progress = serializer.save()
                # 记录创建案件进展的日志
                ActionLog.objects.create(user=request.user, action=f"Created new progress for event - ID: {event_id}")
                
                success_response = {
                    'success': True,
                    'message': 'Case progress updated successfully'
                }
                print(f"CaseProgressViewSet: Progress created successfully for event {event_id}")
                return Response(success_response)
                
            error_response = {
                'success': False,
                'message': serializer.errors
            }
            print(f"CaseProgressViewSet: Validation error - {serializer.errors}")
            return Response(error_response, status=400)
            
        except CrimeEvent.DoesNotExist:
            error_response = {
                'success': False,
                'message': 'Event not found'
            }
            print(f"CaseProgressViewSet: Event {event_id} not found")
            return Response(error_response, status=404)
        

# 搜索相关视图
class SearchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='crime-types')
    def search_crime_types(self, request):
        """搜索犯罪类型"""
        query = request.query_params.get('query', '')
        crime_types = CrimeType.objects.filter(type_name__icontains=query)
        
        # 记录搜索犯罪类型的日志
        ActionLog.objects.create(user=request.user, action=f"Searched crime types with query: {query}")
        
        data = [{
            'type_code': ct.type_code,  # 使用 type_code 替代 id
            'type_name': ct.type_name,
            'type_description': ct.type_description
        } for ct in crime_types]
        return Response({'results': data})

    @action(detail=False, methods=['get'], url_path='persons') 
    def search_persons(self, request):
        """搜索人员"""
        query = request.query_params.get('query', '')
        persons = Resident.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(person_id__icontains=query)
        )
        
        # 记录搜索人员的日志
        ActionLog.objects.create(user=request.user, action=f"Searched persons with query: {query}")
        
        data = [{
            'person_id': p.person_id,  # 使用 person_id 替代 id
            'name': f"{p.first_name} {p.last_name}",
            'person_id': p.person_id
        } for p in persons]
        return Response({'results': data})

    @action(detail=False, methods=['get'], url_path='weapons')
    def search_weapons(self, request):
        """搜索武器类型"""
        query = request.query_params.get('query', '')
        weapons = Weapon.objects.filter(weapon_description__icontains=query)
        
        # 记录搜索武器的日志
        ActionLog.objects.create(user=request.user, action=f"Searched weapons with query: {query}")
        
        data = [{
            'weapon_code': w.weapon_code,  # 使用 weapon_code 替代 id
            'weapon_description': w.weapon_description
        } for w in weapons]
        return Response({'results': data})

    @action(detail=False, methods=['get'], url_path='blocks')
    def search_blocks(self, request):
        """搜索区块信息"""
        query = request.query_params.get('query', '')
        blocks = Block.objects.filter(
            Q(block_name__icontains=query) |
            Q(domain_description__icontains=query)
        )
        
        # 记录搜索区块的日志
        ActionLog.objects.create(user=request.user, action=f"Searched blocks with query: {query}")
        
        data = [{
            'block_name': b.block_name,
            'block_description': b.domain_description
        } for b in blocks]
        return Response({'results': data})

    @action(detail=False, methods=['post'], url_path='add-crime-type')
    def add_crime_type(self, request):
        """添加新的犯罪类型"""
        type_name = request.data.get('type_name')
        type_description = request.data.get('type_description', '')
        
        if not type_name:
            return Response({'error': '犯罪类型名称不能为空'}, status=400)
            
        if CrimeType.objects.filter(type_name=type_name).exists():
            return Response({'error': '该犯罪类型已存在'}, status=400)
        
        # type_code会自动生成,is_active设为True
        crime_type = CrimeType.objects.create(
            type_name=type_name,
            type_description=type_description,
            is_active=True
        )
        
        # 记录添加犯罪类型的日志
        ActionLog.objects.create(user=request.user, action=f"Added new crime type: {type_name}")

        return Response({
            'success': True,
            'message': '添加成功',
            'data': {
                'type_code': crime_type.type_code,  # 返回自动生成的type_code
                'type_name': crime_type.type_name,
                'type_description': crime_type.type_description,
                'is_active': crime_type.is_active
            }
        })