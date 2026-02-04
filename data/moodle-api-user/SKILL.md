---
name: moodle-api-user
description: Interact with the MicroTutor Moodle LMS via REST API to manage courses, users, enrollments, assignments, quizzes, forums, and grades. Use when the user says "use the api" or asks to query, create, update, or manage any Moodle content including course data, student enrollments, activity modules, submissions, or grades.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Moodle API User Skill

This skill enables Claude to interact with the MicroTutor Moodle LMS (microtutorcourses.org) via its REST API. It provides access to 416+ web service functions for comprehensive course management and content operations.

## API Configuration

The Moodle REST API is configured via environment variables:

- **MOODLE_API_URL:** `https://microtutorcourses.org`
- **MOODLE_API_TOKEN:** Web service token (stored in environment)

## When to Use This Skill

Activate this skill when the user requests to:

- List, search, or retrieve course information
- Get enrolled users or manage enrollments
- Access course contents, sections, and activities
- Retrieve or manage assignments and submissions
- Work with quizzes, forums, or other activity modules
- Query grades or completion data
- Manage users or check user profiles
- Access H5P activities or interactive content
- Create, update, or delete course content

## API Call Format

All Moodle REST API calls follow this pattern:

```bash
curl -X POST "${MOODLE_API_URL}/webservice/rest/server.php" \
  -d "wstoken=${MOODLE_API_TOKEN}" \
  -d "wsfunction=<function_name>" \
  -d "moodlewsrestformat=json" \
  -d "<parameter1>=<value1>" \
  -d "<parameter2>=<value2>"
```

The response is always JSON.

### Core Functions (165 functions)

- **Courses:** `core_course_*` - Course management, contents, navigation
- **Users:** `core_user_*` - User profiles, preferences, files
- **Enrollments:** `core_enrol_*` - Enrollment queries and management
- **Grades:** `core_grades_*` - Grade items, panels, reports
- **Calendar:** `core_calendar_*` - Events, views, access
- **Messages:** `core_message_*` - Messaging and notifications
- **Comments:** `core_comment_*` - Comment operations
- **Completion:** `core_completion_*` - Course and activity completion
- **Groups:** `core_group_*` - Group management
- **Files:** `core_files_*` - File operations

### Activity Module Functions (209 functions)

- **Assignments:** `mod_assign_*` - Assignment management, submissions, grading
- **Quizzes:** `mod_quiz_*` - Quiz attempts, questions, grades
- **Forums:** `mod_forum_*` - Discussions, posts, subscriptions
- **H5P:** `mod_h5pactivity_*` - Interactive content, attempts, results
- **Books:** `mod_book_*` - Book resources
- **Glossaries:** `mod_glossary_*` - Glossary entries
- **Wikis:** `mod_wiki_*` - Wiki pages and collaboration
- **Workshops:** `mod_workshop_*` - Peer assessment activities
- **Lessons:** `mod_lesson_*` - Lesson activities
- **Folders/Pages/Resources:** `mod_folder_*`, `mod_page_*`, `mod_resource_*`
- **SCORM:** `mod_scorm_*` - SCORM packages
- **Feedback:** `mod_feedback_*` - Feedback activities
- **Chat/Choice/Survey/Data:** Various communication and data collection modules

### Other Functions

- **Enrollment plugins:** `enrol_*` - Guest and self-enrollment
- **Reports:** `report_*`, `gradereport_*` - Analytics and grade reports
- **Tools:** `tool_*` - Mobile, analytics, competencies, Moodle.net
- **Blocks:** `block_*` - Recently accessed items, starred courses
- **Messages:** `message_*` - Notification preferences

## Examples

### Example 1: Get Site Information

```bash
curl -X POST "${MOODLE_API_URL}/webservice/rest/server.php" \
  -d "wstoken=${MOODLE_API_TOKEN}" \
  -d "wsfunction=core_webservice_get_site_info" \
  -d "moodlewsrestformat=json"
```

### Example 2: List All Courses

```bash
curl -X POST "${MOODLE_API_URL}/webservice/rest/server.php" \
  -d "wstoken=${MOODLE_API_TOKEN}" \
  -d "wsfunction=core_course_get_courses" \
  -d "moodlewsrestformat=json"
```

### Example 3: Get Course Contents

```bash
curl -X POST "${MOODLE_API_URL}/webservice/rest/server.php" \
  -d "wstoken=${MOODLE_API_TOKEN}" \
  -d "wsfunction=core_course_get_contents" \
  -d "courseid=${MOODLE_COURSE_ID}" \
  -d "moodlewsrestformat=json"
```

## Best Practices

NEVER make destructive changes without explicit user instructions. Follow these best practices:

1. **Always check permissions first** - Use access information functions before attempting operations
2. **Handle pagination** - Many list functions support limitfrom/limitnum parameters
3. **Use specific functions** - Prefer specific functions over generic ones for better performance
4. **Parse JSON responses** - Use `jq` or Python for clean JSON handling
5. **Log errors** - Capture error responses for debugging
6. **Respect rate limits** - Be mindful of API load on the production server

## Security Notes

- **Never commit the token** - Always use `MOODLE_API_TOKEN` environment variable, never hardcode tokens
- **Store in .env** - Keep tokens in `.env` file (add to `.gitignore`)
- **Read-only by default** - Most operations are read-only; write operations require appropriate permissions
- **Audit write operations** - Changes made via API are logged to Moodle's activity logs
- **Token scope** - The current token has access to the full "Moodle mobile web service" (416 functions)
- **Revoke if compromised** - Tokens can be revoked via Moodle admin interface

## List of All Functions

From <https://microtutorcourses.org/admin/webservice/documentation.php>

- `block_recentlyaccesseditems_get_recent_items`
- `block_starredcourses_get_starred_courses`
- `core_badges_get_user_badge_by_hash`
- `core_badges_get_user_badges`
- `core_block_fetch_addable_blocks`
- `core_block_get_course_blocks`
- `core_block_get_dashboard_blocks`
- `core_blog_get_entries`
- `core_blog_view_entries`
- `core_calendar_create_calendar_events`
- `core_calendar_delete_calendar_events`
- `core_calendar_get_action_events_by_course`
- `core_calendar_get_action_events_by_courses`
- `core_calendar_get_action_events_by_timesort`
- `core_calendar_get_allowed_event_types`
- `core_calendar_get_calendar_access_information`
- `core_calendar_get_calendar_day_view`
- `core_calendar_get_calendar_event_by_id`
- `core_calendar_get_calendar_events`
- `core_calendar_get_calendar_export_token`
- `core_calendar_get_calendar_monthly_view`
- `core_calendar_get_calendar_upcoming_view`
- `core_calendar_submit_create_update_form`
- `core_calendar_update_event_start_day`
- `core_comment_add_comments`
- `core_comment_delete_comments`
- `core_comment_get_comments`
- `core_competency_competency_viewed`
- `core_competency_delete_evidence`
- `core_competency_get_scale_values`
- `core_competency_grade_competency_in_course`
- `core_competency_list_course_competencies`
- `core_competency_user_competency_plan_viewed`
- `core_competency_user_competency_viewed`
- `core_competency_user_competency_viewed_in_course`
- `core_competency_user_competency_viewed_in_plan`
- `core_completion_get_activities_completion_status`
- `core_completion_get_course_completion_status`
- `core_completion_mark_course_self_completed`
- `core_completion_update_activity_completion_status_manually`
- `core_course_check_updates`
- `core_course_get_categories`
- `core_course_get_contents`
- `core_course_get_course_module`
- `core_course_get_course_module_by_instance`
- `core_course_get_courses`
- `core_course_get_courses_by_field`
- `core_course_get_enrolled_courses_by_timeline_classification`
- `core_course_get_enrolled_courses_with_action_events_by_timeline_classification`
- `core_course_get_recent_courses`
- `core_course_get_updates_since`
- `core_course_get_user_administration_options`
- `core_course_get_user_navigation_options`
- `core_course_search_courses`
- `core_course_set_favourite_courses`
- `core_course_view_course`
- `core_enrol_get_course_enrolment_methods`
- `core_enrol_get_enrolled_users`
- `core_enrol_get_users_courses`
- `core_enrol_search_users`
- `core_files_delete_draft_files`
- `core_files_get_files`
- `core_files_get_unused_draft_itemid`
- `core_filters_get_available_in_context`
- `core_get_component_strings`
- `core_grades_get_enrolled_users_for_search_widget`
- `core_grades_get_enrolled_users_for_selector`
- `core_grades_get_gradable_users`
- `core_grades_get_gradeitems`
- `core_grades_get_groups_for_search_widget`
- `core_grades_get_groups_for_selector`
- `core_grades_grader_gradingpanel_point_fetch`
- `core_grades_grader_gradingpanel_point_store`
- `core_grades_grader_gradingpanel_scale_fetch`
- `core_grades_grader_gradingpanel_scale_store`
- `core_group_get_activity_allowed_groups`
- `core_group_get_activity_groupmode`
- `core_group_get_course_groupings`
- `core_group_get_course_groups`
- `core_group_get_course_user_groups`
- `core_group_get_groups_for_selector`
- `core_h5p_get_trusted_h5p_file`
- `core_message_block_user`
- `core_message_confirm_contact_request`
- `core_message_create_contact_request`
- `core_message_data_for_messagearea_search_messages`
- `core_message_decline_contact_request`
- `core_message_delete_contacts`
- `core_message_delete_conversations_by_id`
- `core_message_delete_message`
- `core_message_delete_message_for_all_users`
- `core_message_get_blocked_users`
- `core_message_get_contact_requests`
- `core_message_get_conversation`
- `core_message_get_conversation_between_users`
- `core_message_get_conversation_counts`
- `core_message_get_conversation_members`
- `core_message_get_conversation_messages`
- `core_message_get_conversations`
- `core_message_get_member_info`
- `core_message_get_messages`
- `core_message_get_received_contact_requests_count`
- `core_message_get_self_conversation`
- `core_message_get_unread_conversation_counts`
- `core_message_get_unread_conversations_count`
- `core_message_get_unread_notification_count`
- `core_message_get_user_contacts`
- `core_message_get_user_message_preferences`
- `core_message_get_user_notification_preferences`
- `core_message_mark_all_conversation_messages_as_read`
- `core_message_mark_all_notifications_as_read`
- `core_message_mark_message_read`
- `core_message_mark_notification_read`
- `core_message_message_processor_config_form`
- `core_message_message_search_users`
- `core_message_mute_conversations`
- `core_message_search_contacts`
- `core_message_send_instant_messages`
- `core_message_send_messages_to_conversation`
- `core_message_set_favourite_conversations`
- `core_message_unblock_user`
- `core_message_unmute_conversations`
- `core_message_unset_favourite_conversations`
- `core_my_view_page`
- `core_notes_create_notes`
- `core_notes_delete_notes`
- `core_notes_get_course_notes`
- `core_notes_view_notes`
- `core_question_update_flag`
- `core_rating_add_rating`
- `core_rating_get_item_ratings`
- `core_reportbuilder_can_view_system_report`
- `core_reportbuilder_list_reports`
- `core_reportbuilder_retrieve_report`
- `core_reportbuilder_retrieve_system_report`
- `core_reportbuilder_view_report`
- `core_search_get_results`
- `core_search_get_search_areas_list`
- `core_search_get_top_results`
- `core_search_view_results`
- `core_table_get_dynamic_table_content`
- `core_tag_get_tag_areas`
- `core_tag_get_tag_cloud`
- `core_tag_get_tag_collections`
- `core_tag_get_tagindex`
- `core_tag_get_tagindex_per_area`
- `core_user_add_user_device`
- `core_user_add_user_private_files`
- `core_user_agree_site_policy`
- `core_user_get_course_user_profiles`
- `core_user_get_private_files_info`
- `core_user_get_user_preferences`
- `core_user_get_users_by_field`
- `core_user_remove_user_device`
- `core_user_set_user_preferences`
- `core_user_update_picture`
- `core_user_update_user_device_public_key`
- `core_user_update_user_preferences`
- `core_user_view_user_list`
- `core_user_view_user_profile`
- `core_webservice_get_site_info`
- `core_xapi_delete_state`
- `core_xapi_delete_states`
- `core_xapi_get_state`
- `core_xapi_get_states`
- `core_xapi_post_state`
- `core_xapi_statement_post`
- `enrol_guest_get_instance_info`
- `enrol_guest_validate_password`
- `enrol_self_enrol_user`
- `enrol_self_get_instance_info`
- `gradereport_grader_get_users_in_report`
- `gradereport_overview_get_course_grades`
- `gradereport_overview_view_grade_report`
- `gradereport_singleview_get_grade_items_for_search_widget`
- `gradereport_user_get_access_information`
- `gradereport_user_get_grade_items`
- `gradereport_user_get_grades_table`
- `gradereport_user_view_grade_report`
- `message_airnotifier_are_notification_preferences_configured`
- `message_airnotifier_enable_device`
- `message_airnotifier_get_user_devices`
- `message_airnotifier_is_system_configured`
- `message_popup_get_popup_notifications`
- `message_popup_get_unread_popup_notification_count`
- `mod_assign_get_assignments`
- `mod_assign_get_grades`
- `mod_assign_get_participant`
- `mod_assign_get_submission_status`
- `mod_assign_get_submissions`
- `mod_assign_get_user_flags`
- `mod_assign_get_user_mappings`
- `mod_assign_list_participants`
- `mod_assign_lock_submissions`
- `mod_assign_reveal_identities`
- `mod_assign_revert_submissions_to_draft`
- `mod_assign_save_grade`
- `mod_assign_save_grades`
- `mod_assign_save_submission`
- `mod_assign_save_user_extensions`
- `mod_assign_set_user_flags`
- `mod_assign_start_submission`
- `mod_assign_submit_for_grading`
- `mod_assign_submit_grading_form`
- `mod_assign_unlock_submissions`
- `mod_assign_view_assign`
- `mod_assign_view_grading_table`
- `mod_assign_view_submission_status`
- `mod_bigbluebuttonbn_can_join`
- `mod_bigbluebuttonbn_completion_validate`
- `mod_bigbluebuttonbn_end_meeting`
- `mod_bigbluebuttonbn_get_bigbluebuttonbns_by_courses`
- `mod_bigbluebuttonbn_get_join_url`
- `mod_bigbluebuttonbn_get_recordings`
- `mod_bigbluebuttonbn_get_recordings_to_import`
- `mod_bigbluebuttonbn_meeting_info`
- `mod_bigbluebuttonbn_update_recording`
- `mod_bigbluebuttonbn_view_bigbluebuttonbn`
- `mod_book_get_books_by_courses`
- `mod_book_view_book`
- `mod_chat_get_chat_latest_messages`
- `mod_chat_get_chat_users`
- `mod_chat_get_chats_by_courses`
- `mod_chat_get_session_messages`
- `mod_chat_get_sessions`
- `mod_chat_login_user`
- `mod_chat_send_chat_message`
- `mod_chat_view_chat`
- `mod_chat_view_sessions`
- `mod_choice_delete_choice_responses`
- `mod_choice_get_choice_options`
- `mod_choice_get_choice_results`
- `mod_choice_get_choices_by_courses`
- `mod_choice_submit_choice_response`
- `mod_choice_view_choice`
- `mod_data_add_entry`
- `mod_data_approve_entry`
- `mod_data_delete_entry`
- `mod_data_get_data_access_information`
- `mod_data_get_databases_by_courses`
- `mod_data_get_entries`
- `mod_data_get_entry`
- `mod_data_get_fields`
- `mod_data_search_entries`
- `mod_data_update_entry`
- `mod_data_view_database`
- `mod_feedback_get_analysis`
- `mod_feedback_get_current_completed_tmp`
- `mod_feedback_get_feedback_access_information`
- `mod_feedback_get_feedbacks_by_courses`
- `mod_feedback_get_finished_responses`
- `mod_feedback_get_items`
- `mod_feedback_get_last_completed`
- `mod_feedback_get_non_respondents`
- `mod_feedback_get_page_items`
- `mod_feedback_get_responses_analysis`
- `mod_feedback_get_unfinished_responses`
- `mod_feedback_launch_feedback`
- `mod_feedback_process_page`
- `mod_feedback_view_feedback`
- `mod_folder_get_folders_by_courses`
- `mod_folder_view_folder`
- `mod_forum_add_discussion`
- `mod_forum_add_discussion_post`
- `mod_forum_can_add_discussion`
- `mod_forum_delete_post`
- `mod_forum_get_discussion_post`
- `mod_forum_get_discussion_posts`
- `mod_forum_get_forum_access_information`
- `mod_forum_get_forum_discussions`
- `mod_forum_get_forum_discussions_paginated`
- `mod_forum_get_forums_by_courses`
- `mod_forum_prepare_draft_area_for_post`
- `mod_forum_set_lock_state`
- `mod_forum_set_pin_state`
- `mod_forum_set_subscription_state`
- `mod_forum_toggle_favourite_state`
- `mod_forum_update_discussion_post`
- `mod_forum_view_forum`
- `mod_forum_view_forum_discussion`
- `mod_glossary_add_entry`
- `mod_glossary_delete_entry`
- `mod_glossary_get_authors`
- `mod_glossary_get_categories`
- `mod_glossary_get_entries_by_author`
- `mod_glossary_get_entries_by_author_id`
- `mod_glossary_get_entries_by_category`
- `mod_glossary_get_entries_by_date`
- `mod_glossary_get_entries_by_letter`
- `mod_glossary_get_entries_by_search`
- `mod_glossary_get_entries_by_term`
- `mod_glossary_get_entries_to_approve`
- `mod_glossary_get_entry_by_id`
- `mod_glossary_get_glossaries_by_courses`
- `mod_glossary_prepare_entry_for_edition`
- `mod_glossary_update_entry`
- `mod_glossary_view_entry`
- `mod_glossary_view_glossary`
- `mod_h5pactivity_get_attempts`
- `mod_h5pactivity_get_h5pactivities_by_courses`
- `mod_h5pactivity_get_h5pactivity_access_information`
- `mod_h5pactivity_get_results`
- `mod_h5pactivity_get_user_attempts`
- `mod_h5pactivity_log_report_viewed`
- `mod_h5pactivity_view_h5pactivity`
- `mod_imscp_get_imscps_by_courses`
- `mod_imscp_view_imscp`
- `mod_label_get_labels_by_courses`
- `mod_lesson_finish_attempt`
- `mod_lesson_get_attempts_overview`
- `mod_lesson_get_content_pages_viewed`
- `mod_lesson_get_lesson`
- `mod_lesson_get_lesson_access_information`
- `mod_lesson_get_lessons_by_courses`
- `mod_lesson_get_page_data`
- `mod_lesson_get_pages`
- `mod_lesson_get_pages_possible_jumps`
- `mod_lesson_get_questions_attempts`
- `mod_lesson_get_user_attempt`
- `mod_lesson_get_user_attempt_grade`
- `mod_lesson_get_user_grade`
- `mod_lesson_get_user_timers`
- `mod_lesson_launch_attempt`
- `mod_lesson_process_page`
- `mod_lesson_view_lesson`
- `mod_lti_get_ltis_by_courses`
- `mod_lti_get_tool_launch_data`
- `mod_lti_view_lti`
- `mod_page_get_pages_by_courses`
- `mod_page_view_page`
- `mod_quiz_get_attempt_access_information`
- `mod_quiz_get_attempt_data`
- `mod_quiz_get_attempt_review`
- `mod_quiz_get_attempt_summary`
- `mod_quiz_get_combined_review_options`
- `mod_quiz_get_quiz_access_information`
- `mod_quiz_get_quiz_feedback_for_grade`
- `mod_quiz_get_quiz_required_qtypes`
- `mod_quiz_get_quizzes_by_courses`
- `mod_quiz_get_user_attempts`
- `mod_quiz_get_user_best_grade`
- `mod_quiz_process_attempt`
- `mod_quiz_save_attempt`
- `mod_quiz_start_attempt`
- `mod_quiz_view_attempt`
- `mod_quiz_view_attempt_review`
- `mod_quiz_view_attempt_summary`
- `mod_quiz_view_quiz`
- `mod_resource_get_resources_by_courses`
- `mod_resource_view_resource`
- `mod_scorm_get_scorm_access_information`
- `mod_scorm_get_scorm_attempt_count`
- `mod_scorm_get_scorm_sco_tracks`
- `mod_scorm_get_scorm_scoes`
- `mod_scorm_get_scorm_user_data`
- `mod_scorm_get_scorms_by_courses`
- `mod_scorm_insert_scorm_tracks`
- `mod_scorm_launch_sco`
- `mod_scorm_view_scorm`
- `mod_survey_get_questions`
- `mod_survey_get_surveys_by_courses`
- `mod_survey_submit_answers`
- `mod_survey_view_survey`
- `mod_url_get_urls_by_courses`
- `mod_url_view_url`
- `mod_wiki_edit_page`
- `mod_wiki_get_page_contents`
- `mod_wiki_get_page_for_editing`
- `mod_wiki_get_subwiki_files`
- `mod_wiki_get_subwiki_pages`
- `mod_wiki_get_subwikis`
- `mod_wiki_get_wikis_by_courses`
- `mod_wiki_new_page`
- `mod_wiki_view_page`
- `mod_wiki_view_wiki`
- `mod_workshop_add_submission`
- `mod_workshop_delete_submission`
- `mod_workshop_evaluate_assessment`
- `mod_workshop_evaluate_submission`
- `mod_workshop_get_assessment`
- `mod_workshop_get_assessment_form_definition`
- `mod_workshop_get_grades`
- `mod_workshop_get_grades_report`
- `mod_workshop_get_reviewer_assessments`
- `mod_workshop_get_submission`
- `mod_workshop_get_submission_assessments`
- `mod_workshop_get_submissions`
- `mod_workshop_get_user_plan`
- `mod_workshop_get_workshop_access_information`
- `mod_workshop_get_workshops_by_courses`
- `mod_workshop_update_assessment`
- `mod_workshop_update_submission`
- `mod_workshop_view_submission`
- `mod_workshop_view_workshop`
- `report_insights_action_executed`
- `report_insights_set_fixed_prediction`
- `report_insights_set_notuseful_prediction`
- `tool_analytics_potential_contexts`
- `tool_lp_data_for_course_competencies_page`
- `tool_lp_data_for_plan_page`
- `tool_lp_data_for_plans_page`
- `tool_lp_data_for_user_competency_summary`
- `tool_lp_data_for_user_competency_summary_in_course`
- `tool_lp_data_for_user_competency_summary_in_plan`
- `tool_lp_data_for_user_evidence_list_page`
- `tool_lp_data_for_user_evidence_page`
- `tool_mobile_call_external_functions`
- `tool_mobile_get_autologin_key`
- `tool_mobile_get_config`
- `tool_mobile_get_content`
- `tool_mobile_get_plugins_supporting_mobile`
- `tool_mobile_get_public_config`
- `tool_mobile_get_tokens_for_qr_login`
- `tool_mobile_validate_subscription_key`
- `tool_moodlenet_search_courses`
- `tool_moodlenet_verify_webfinger`
