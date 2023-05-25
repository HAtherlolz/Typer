from sqladmin import ModelView

from app.models import Profile, Language, Time, Lesson, Training


class ProfileAdmin(ModelView, model=Profile):
    name = "Profile"
    name_plural = "Profiles"
    icon = "fa-solid fa-person"
    column_list = [Profile.id, Profile.email, Profile.nickname]
    column_searchable_list = [Profile.id, Profile.email, Profile.nickname]


class LanguageAdmin(ModelView, model=Language):
    name = "Language"
    name_plural = "Languages"
    icon = "fa-solid fa-language"
    column_list = [Language.id, Language.name]
    column_searchable_list = [Language.id, Language.name]


class TimeAdmin(ModelView, model=Time):
    name = "Time"
    name_plural = "Times"
    icon = "fa-solid fa-code"
    column_list = [Time.id, Time.seconds]
    column_searchable_list = [Time.id, Time.seconds]


class LessonAdmin(ModelView, model=Lesson):
    name = "Lesson"
    name_plural = "Lessons"
    icon = "fa-solid fa-address-book"
    column_list = [Lesson.id, Lesson.name, Lesson.language]
    column_searchable_list = [
        Lesson.id, Lesson.name, Lesson.seconds_spent, Lesson.wpm, Lesson.cpm,
        Lesson.row_wpm, Lesson.accuracy, Lesson.consistency,
        Lesson.date_time
    ]


class TrainingAdmin(ModelView, model=Training):

    def profile_formatter(self, profile):
        return profile.email

    name = "Training"
    name_plural = "Trainings"
    icon = "fa-solid fa-sitemap"
    column_formatters = {Training.profile: profile_formatter}
    column_list = [Training.id, Training.profile, Training.training_language]
    column_searchable_list = [
        Training.id, Training.wpm, Training.cpm,
        Training.row_wpm, Training.accuracy, Training.consistency,
        Training.date_time
    ]

# Add all created admins view to list


admins_models = [
    ProfileAdmin, LanguageAdmin, TimeAdmin,
    LessonAdmin, TrainingAdmin

]
