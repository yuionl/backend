-- 清理数据库数据的SQL脚本
-- 按照外键依赖顺序删除数据

-- 1. 答题记录
DELETE FROM user_app_answerrecord;

-- 2. 任务题目关联表
DELETE FROM user_app_task_questions;

-- 3. 任务
DELETE FROM user_app_task;

-- 4. 课堂
DELETE FROM user_app_classroom;

-- 5. 课程学生关系
DELETE FROM user_app_coursestudent;

-- 6. 题目
DELETE FROM user_app_question;

-- 7. 课程
DELETE FROM user_app_course;

-- 8. 用户
DELETE FROM user_app_user;

-- 重置自增ID
ALTER TABLE user_app_user AUTO_INCREMENT = 1;
ALTER TABLE user_app_question AUTO_INCREMENT = 1;
ALTER TABLE user_app_course AUTO_INCREMENT = 1;
ALTER TABLE user_app_coursestudent AUTO_INCREMENT = 1;
ALTER TABLE user_app_classroom AUTO_INCREMENT = 1;
ALTER TABLE user_app_task AUTO_INCREMENT = 1;
ALTER TABLE user_app_answerrecord AUTO_INCREMENT = 1;

-- 提交事务
COMMIT;

SELECT '数据库清理完成' AS message;
