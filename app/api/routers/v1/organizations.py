# ruff:noqa:UP045,B008
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import Field

from app.core import BusinessException, NotFoundException
from app.core.dependencies.services import OrganizationService, get_organization_service
from app.schemas import (
    CoordinateRadius,
    CoordinateRectangle,
    Organization,
    OrganizationCreate,
)

router = APIRouter(prefix="/organization", tags=["organization"])


@router.get("/radius", response_model=list[Organization])
async def get_organizations_by_radius(
    lat: Annotated[float, Query(..., description="Latitude")],
    lon: Annotated[float, Query(..., description="Longitude")],
    radius_km: Annotated[float | int, Query(..., description="Radius in km")],
    organization_service: OrganizationService = Depends(get_organization_service),
) -> list[Organization]:
    """
    Поиск организаций в заданном радиусе от географической точки.

    Использует формулу гаверсинуса для расчета расстояния между координатами
    и возвращает все активные организации, находящиеся в пределах указанного
    радиуса от заданной точки(погрешность примерно 300-400 метров).
    Поиск учитывает как точное расположение зданий, так и статус активности организаций.

    Args:
        lat: Географическая широта центра поиска в градусах(от -90 до 90)
        lon: Географическая долгота центра поиска в градусах(от -90 до 90)
        radius_km: Радиус поиска в километрах(радиус землю 6371 км) максимально
        organization_service: Сервисный слой для работы с организациями,
                             реализующий геопоиск и аркестрирующий бизнес-логику,
                             управляет конкретными use-cases.

    Raises:
        HTTPException: 404 Not Found - когда в указанном радиусе не найдено
                      ни одной активной организации
        HTTPException: 401 Unauthorizated - когда api key не совпадает или не указан

    Returns:
        Список организаций, удовлетворяющих критериям поиска по радиусу,
        с полной информацией о зданиях и видах деятельности
    """
    try:
        coordinates = CoordinateRadius(lat=lat, lon=lon, radius_km=radius_km)
        return await organization_service.get_organization_by_radius(coordinates)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get("/area/", response_model=list[Organization])
async def get_organizations_by_rectangle(
    lat_min: Annotated[float, Query(..., description="Min latitude")],
    lat_max: Annotated[float, Query(..., description="Max latitude")],
    lon_min: Annotated[float, Query(..., description="Min longitude")],
    lon_max: Annotated[float, Query(..., description="Max longitude")],
    organization_service: OrganizationService = Depends(get_organization_service),
) -> list[Organization]:
    """
    Поиск организаций в заданном прямоугольном географическом области.

    Возвращает все активные организации, расположенные в пределах прямоугольной
    области, ограниченной минимальными и максимальными значениями широты и долготы.
    Поиск оптимизирован для работы с большими наборами географических данных.

    Args:
        lat_min: Минимальное значение широты для ограничения области поиска(от -90 до 90)
        lat_max: Максимальное значение широты для ограничения области поиска(от -90 до 90)
        lon_min: Минимальное значение долготы для ограничения области поиска(от -90 до 90)
        lon_max: Максимальное значение долготы для ограничения области поиска(от -90 до 90)
        organization_service: Сервисный слой для работы с организациями

    Raises:
        HTTPException: 404 Not Found - когда в указанной области не найдено
                      ни одной активной организации
        HTTPException: 401 Unauthorizated - когда api key не совпадает или не указан

    Returns:
        Список организаций, расположенных в заданной прямоугольной области,
        с полной информацией о зданиях и видах деятельности
    """
    try:
        coordinates = CoordinateRectangle(lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)
        return await organization_service.get_organization_by_rectangle(coordinates)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get("/", response_model=list[Organization], status_code=status.HTTP_200_OK)
async def get_organizations(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[Organization]:
    """
    Получает полный список всех активных организаций из системы.

    Возвращает все организации с флагом is_active=True(Не удаленные), включая полную информацию
    о связанных зданиях, видах деятельности и контактных данных.

    Args:
        organization_service: Сервисный слой для работы с организациями,
                             инкапсулирующий бизнес-логику и взаимодействие с БД
    Raises:
        HTTPException: 401 Unauthorizated - когда api key не совпадает или не указан

    Returns:
        Список всех активных организаций в формате Pydantic схем, содержащих
        полную информацию о каждой организации и ее связях
    """
    return await organization_service.get_all_organizations()


@router.get(
    "/{organization_id}",
    response_model=Optional[Organization],
    status_code=status.HTTP_200_OK,
)
async def get_organization(
    organization_id: Annotated[int, Path(ge=1)],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> Organization | None:
    """
    Получает детальную информацию о конкретной организации по ее идентификатору.

    Ищет организацию в системе по уникальному числовому идентификатору. Возвращает
    полные данные об организации включая информацию о здании, видах деятельности
    и контактных телефонах. Поиск ограничен только активными организациями.

    Args:
        organization_id: Уникальный числовой идентификатор организации.
                        Должен быть положительным целым числом больше или равным 1
        organization_service: Сервисный слой для работы с организациями,
                             обеспечивающий поиск и валидацию существования

    Raises:
        HTTPException: 404 Not Found - когда организация с указанным ID не существует
                      в системе или была удалена
        HTTPException: 401 Unauthorizated - когда api key не совпадает или не указан

    Returns:
        Объект Organization с детальной информацией об организации или None,
        если организация не найдена (с последующим возбуждением исключения)
    """
    try:
        return await organization_service.get_organization_by_id(organization_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get(
    "/buildings/{building_id}",
    response_model=list[Organization],
    status_code=status.HTTP_200_OK,
)
async def get_organizations_by_building(
    building_id: Annotated[int, Path(ge=1)],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[Organization]:
    """
    Получает список организаций, расположенных в указанном здании.

    Возвращает все активные организации, связанные с конкретным зданием
    по его идентификатору. Включает организации различных видов деятельности,
    находящиеся в одном физическом местоположении.

    Args:
        building_id: Уникальный числовой идентификатор здания.
                    Должен соответствовать существующему активному зданию
        organization_service: Сервисный слой для работы с организациями,
                             аркестрирующий фильтрацию по связанным объектам

    Raises:
        HTTPException: 404 Not Found - когда здание с указанным ID не найдено
                      или в нем нет активных организаций
        HTTPException: 401 Unauthorizated - когда api key не совпадает или не указан

    Returns:
        Список организаций, расположенных в указанном здании, с полной
        информацией о видах деятельности и контактных данных
    """
    try:
        return await organization_service.get_organization_by_building(building_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get(
    "/activities/{activity_id}",
    response_model=list[Organization],
    status_code=status.HTTP_200_OK,
)
async def get_organizations_by_activity(
    activity_id: Annotated[int, Path(ge=1)],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[Organization]:
    """
    Получает список организаций, связанных с указанным видом деятельности.

    Возвращает все активные организации, которые имеют связь с конкретным
    видом деятельности по его идентификатору. Позволяет фильтровать организации
    по их основной или дополнительной специализации.

    Args:
        activity_id: Уникальный числовой идентификатор вида деятельности.
                    Должен соответствовать существующей активной деятельности
        organization_service: Сервисный слой для работы с организациями,
                            аркестрирующий фильтрацию по связанным активностям

    Raises:
        HTTPException: 404 Not Found - когда вид деятельности с указанным ID
                      не найден или с ним не связано ни одной активной организации
        HTTPException: 401 Unauthorizated - когда api key не совпадает или не указан

    Returns:
        Список организаций, связанных с указанным видом деятельности,
        с полной информацией о зданиях и контактных данных
    """
    try:
        return await organization_service.get_organization_by_activity(activity_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get(
    "/activity/{activity_name}",
    response_model=list[Organization],
    status_code=status.HTTP_200_OK,
)
async def get_organizations_by_activity_with_children(
    activity_name: str,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[Organization]:
    """
    Получает список организаций, связанных с видом деятельности и его дочерними элементами.

    Использует рекурсивный поиск по иерархии видов деятельности для нахождения
    всех организаций, связанных с указанным видом деятельности или любым из
    его дочерних элементов(cte). Подходит для поиска организаций по категориям
    с древовидной структурой.

    Args:
        activity_name: Название родительского вида деятельности для поиска
        organization_service: Сервисный слой для работы с организациями,
                             реализующий use-case-ом рекурсивного поиска по иерархии активностей

    Raises:
        HTTPException: 404 Not Found - когда вид деятельности с указанным названием
                      не найден или с ним не связано ни одной активной организации
        HTTPException: 401 Unauthorizated - когда api key не совпадает или не указан

    Returns:
        Список организаций, связанных с указанным видом деятельности или
        любым из его дочерних элементов в иерархии
    """
    try:
        return await organization_service.get_organizations_by_name_activity_with_children(activity_name)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.post("/", response_model=Optional[Organization], status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization_create: Annotated[OrganizationCreate, Field(description="Organization create data")],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> Organization | None:
    """
    Создает новую организацию в системе.

    Принимает валидированные данные для создания организации, включая название,
    идентификатор здания и список видов деятельности. Автоматически создает
    связи с указанными видами деятельности в промежуточной таблице.

    Args:
        organization_create: Валидированные данные для создания новой организации.
                           Содержит обязательные поля name, building_id и activity_ids
        organization_service: Сервисный слой, отвечающий за бизнес-логику создания
                             и валидацию данных перед сохранением в БД

    Raises:
        HTTPException: 404 Not Found - когда указанные building_id или activity_ids
                      ссылаются на несуществующие объекты
        HTTPException: 400 Bad Request - при нарушении бизнес-правил валидации
                      (дублирование названия, невалидные связи)
        HTTPException: 401 Unauthorizated - когда api key не совпадает или не указан


    Returns:
        Созданный объект Organization с присвоенным идентификатором и всеми полями,
        включая связи с зданием и видами деятельности
    """
    try:
        return await organization_service.create_organization(organization_create)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.put(
    "/{organization_id}",
    response_model=Optional[Organization],
    status_code=status.HTTP_200_OK,
)
async def update_organization(
    organization_id: Annotated[int, Path(ge=1)],
    organization_update: Annotated[OrganizationCreate, Field(description="Building update data")],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> Organization | None:
    """
    Обновляет существующую организацию с указанным идентификатором.

    Позволяет изменить все поля организации: название, привязку к зданию
    и список связанных видов деятельности. Автоматически обновляет связи
    в промежуточной таблице activities на основе предоставленного списка.

    Args:
        organization_id: Уникальный числовой идентификатор обновляемой организации.
                        Должен соответствовать существующей активной записи
        organization_update: Новые данные для обновления организации.
                           Проходит полную валидацию перед применением изменений
        organization_service: Сервисный слой, обеспечивающий бизнес-логику обновления,
                             проверку целостности данных и валидацию связей

    Raises:
        HTTPException: 404 Not Found - когда организация с указанным ID не найдена
                      или указанные building_id/activity_ids не существуют
        HTTPException: 400 Bad Request - при нарушении бизнес-правил валидации
                      (конфликт уникальности, невалидные данные)

    Returns:
        Обновленный объект Organization с примененными изменениями или None
        в случае ошибки обновления (с последующим возбуждением исключения)
    """
    try:
        return await organization_service.update_organization(organization_id, organization_update)
    except (BusinessException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.delete("/{organization_id}")
async def delete_organization(
    organization_id: Annotated[int, Path(ge=1)],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> dict:
    """
    Выполняет мягкое удаление организации по идентификатору.

    Устанавливает флаг is_active=false для указанной организации, что позволяет
    сохранить исторические данные и ссылочную целостность, исключив организацию
    из рабочих процессов. Удаленная организация больше не будет появляться
    в результатах поиска и списках организаций.

    Args:
        organization_id: Уникальный числовой идентификатор удаляемой организации.
                        Должен соответствовать существующей и активной записи
        organization_service: Сервисный слой, реализующий логику мягкого удаления
                             и проверку возможности удаления организации

    Raises:
        HTTPException: 404 Not Found - когда организация с указанным ID не найдена
                      или уже была удалена ранее
        HTTPException: 401 Unauthorizated - когда api key не совпадает или не указан

    Returns:
        Словарь с результатом операции:
        - {"success": "Organization success deleted"} при успешном удалении
        - {"success": "Organization not exists"} при попытке удаления несуществующей организации
    """
    try:
        res = await organization_service.delete_organization(organization_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    if res:
        return {"success": "Organization success deleted"}
    return {"success": "Organization not exists"}
