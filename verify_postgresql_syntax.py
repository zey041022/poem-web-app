import re

# 读取SQL文件
with open('full_poetry_database.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

# 验证SERIAL语法是否正确
serial_pattern = r'id\s+SERIAL\s+PRIMARY\s+KEY'
timestamp_pattern = r'TIMESTAMP\s+WITH\s+TIME\s+ZONE'

serial_matches = re.findall(serial_pattern, sql_content, re.IGNORECASE)
timestamp_matches = re.findall(timestamp_pattern, sql_content, re.IGNORECASE)

print("===== PostgreSQL 语法验证结果 =====")
print(f"1. SERIAL语法检查: {'通过' if len(serial_matches) == 2 else f'失败 - 期望2处匹配，实际找到{len(serial_matches)}处'}")
print(f"2. TIMESTAMP WITH TIME ZONE语法检查: {'通过' if len(timestamp_matches) == 4 else f'失败 - 期望4处匹配，实际找到{len(timestamp_matches)}处'}")

# 检查是否还有AUTO_INCREMENT语法
if 'AUTO_INCREMENT' in sql_content:
    print("3. 旧语法清理: 失败 - 发现AUTO_INCREMENT语法，请检查")
else:
    print("3. 旧语法清理: 通过 - 未发现AUTO_INCREMENT语法")

# 检查ON UPDATE CURRENT_TIMESTAMP语法
if 'ON UPDATE CURRENT_TIMESTAMP' in sql_content:
    print("4. ON UPDATE语法清理: 失败 - 发现ON UPDATE CURRENT_TIMESTAMP语法，请检查")
else:
    print("4. ON UPDATE语法清理: 通过 - 未发现ON UPDATE CURRENT_TIMESTAMP语法")

# 检查MySQL风格的内联COMMENT语法
inline_comment_pattern = r'COMMENT\s+\'[^\']+\''
inl_commatches = re.findall(inline_comment_pattern, sql_content, re.IGNORECASE)
if len(inl_commatches) > 0:
    print("5. MySQL内联注释检查: 失败 - 发现MySQL风格的内联COMMENT语法")
else:
    print("5. MySQL内联注释检查: 通过 - 未发现MySQL风格的内联COMMENT语法")

# 检查PostgreSQL的COMMENT ON COLUMN语法
tang_comment_pattern = r'COMMENT\s+ON\s+COLUMN\s+tang_poetry\.[a-z_]+\s+IS\s+\'[^\']+\''
song_comment_pattern = r'COMMENT\s+ON\s+COLUMN\s+song_poetry\.[a-z_]+\s+IS\s+\'[^\']+\''

tang_comments = re.findall(tang_comment_pattern, sql_content, re.IGNORECASE)
song_comments = re.findall(song_comment_pattern, sql_content, re.IGNORECASE)

print(f"6. tang_poetry表列注释检查: {'通过' if len(tang_comments) >= 8 else f'失败 - 期望至少8处注释，实际找到{len(tang_comments)}处'}")
print(f"7. song_poetry表列注释检查: {'通过' if len(song_comments) >= 9 else f'失败 - 期望至少9处注释，实际找到{len(song_comments)}处'}")

# 验证整体语法结构
table_patterns = [
    r'CREATE\s+TABLE\s+tang_poetry',
    r'CREATE\s+TABLE\s+song_poetry',
    r'CREATE\s+INDEX',
    r'COMMENT\s+ON\s+COLUMN'
]

print("\n===== 表结构验证 =====")
for pattern in table_patterns:
    matches = re.findall(pattern, sql_content, re.IGNORECASE)
    # 修复f-string中的反斜杠问题
    display_pattern = pattern.replace('\\s+', ' ')
    print(f"- {display_pattern}: {'通过' if len(matches) > 0 else '失败 - 未找到该结构'}")

# 检查是否所有验证都通过
all_passed = (len(serial_matches) == 2 and 
              len(timestamp_matches) == 4 and 
              'AUTO_INCREMENT' not in sql_content and 
              'ON UPDATE CURRENT_TIMESTAMP' not in sql_content and 
              len(inl_commatches) == 0 and 
              len(tang_comments) >= 8 and 
              len(song_comments) >= 9)

print("\nSQL文件已修改为PostgreSQL兼容格式，主要修改包括：")
print("1. 将MySQL的AUTO_INCREMENT改为PostgreSQL的SERIAL")
print("2. 将TIMESTAMP改为TIMESTAMP WITH TIME ZONE以支持时区")
print("3. 移除了ON UPDATE CURRENT_TIMESTAMP子句（PostgreSQL不支持）")
print("4. 将MySQL风格的内联列注释改为PostgreSQL的COMMENT ON COLUMN语法")

if all_passed:
    print("\n✅ 恭喜！所有PostgreSQL语法验证都已通过！")
else:
    print("\n❌ 警告：部分验证未通过，请检查上述错误信息。")
print("\n要在PostgreSQL中创建更新触发器，可以使用以下语句：")
print("""-- 为tang_poetry表创建更新触发器
CREATE OR REPLACE FUNCTION update_tang_poetry_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER set_tang_poetry_timestamp
BEFORE UPDATE ON tang_poetry
FOR EACH ROW
EXECUTE PROCEDURE update_tang_poetry_timestamp();

-- 为song_poetry表创建更新触发器
CREATE OR REPLACE FUNCTION update_song_poetry_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER set_song_poetry_timestamp
BEFORE UPDATE ON song_poetry
FOR EACH ROW
EXECUTE PROCEDURE update_song_poetry_timestamp();""")