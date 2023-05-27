from fastapi import APIRouter

from app.endpoints.v1 import profile, language, time, training, lesson

api_router = APIRouter()


api_router.include_router(profile.profile_router, prefix='/api/v1', tags=["profiles"])
api_router.include_router(language.lang_router, prefix='/api/v1', tags=["languages"])
api_router.include_router(time.time_router, prefix='/api/v1', tags=["times"])
api_router.include_router(training.training_router, prefix='/api/v1', tags=["trainings"])
api_router.include_router(lesson.lesson_router, prefix='/api/v1', tags=["lessons"])

