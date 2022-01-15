BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
CREATE TABLE IF NOT EXISTS "crawling" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(200) NOT NULL,
	"link"	TEXT NOT NULL,
	"snippet"	TEXT NOT NULL,
	"pub_date"	TEXT,
	"sni_tran"	TEXT,
	"create_date"	DATETIME NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "article_download" (
	"id"	INTEGER NOT NULL,
	"crawling_id"	INTEGER,
	"summary"	TEXT,
	"sum_tran"	TEXT,
	"body_text"	TEXT,
	"body_tran"	TEXT,
	FOREIGN KEY("crawling_id") REFERENCES "crawling"("id") ON DELETE CASCADE,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "machine_learning" (
	"id"	INTEGER NOT NULL,
	"crawling_id"	INTEGER,
	"news_val"	INTEGER,
	"art_val"	INTEGER,
	"cos_val"	INTEGER,
	"ml_val"	INTEGER,
	FOREIGN KEY("crawling_id") REFERENCES "crawling"("id") ON DELETE CASCADE,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user_data" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER,
	"search_word"	VARCHAR(150),
	CONSTRAINT "fk_user_data_user_id_user" FOREIGN KEY("user_id") REFERENCES "user"("id") ON DELETE CASCADE,
	CONSTRAINT "pk_user_data" PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(150) NOT NULL,
	"password"	VARCHAR(200) NOT NULL,
	"email"	VARCHAR(120) NOT NULL,
	"p_member"	INTEGER,
	"search_word"	VARCHAR(150),
	CONSTRAINT "uq_user_username" UNIQUE("username"),
	CONSTRAINT "uq_user_email" UNIQUE("email"),
	CONSTRAINT "pk_user" PRIMARY KEY("id")
);
INSERT INTO "alembic_version" VALUES ('b34706ddacba');
INSERT INTO "crawling" VALUES (1,'문재인 호주 방문','https://overseas.mofa.go.kr/au-ko/brd/m_3884/view.do?seq=1344798&srchFr=&amp;srchTo=&amp;srchWord=&amp;srchTp=&amp;multi_itm_seq=0&amp;itm_seq_1=0&amp;itm_seq_2=0&amp;company_cd=&amp;company_nm=&page=1','문재인 대통령 호주 국빈 방문 관련',NULL,NULL,'2021-12-29 16:34:39.915468');
INSERT INTO "crawling" VALUES (2,'박근혜 석방','https://www.yna.co.kr/view/AKR20211224039352004','박근혜 특별사면 석방·한명숙 복권…이석기 가석방',NULL,NULL,'2021-12-29 16:35:25.211347');
INSERT INTO "article_download" VALUES (1,2,'문재인 대통령은 ‘스콧 모리슨(Scott Morrison)’ 호주 총리의 초청으로 12월 12일부터 15일까지 3박4일의 일정으로 호주를 국빈 방문할 예정입니다.',NULL,NULL,NULL);
INSERT INTO "article_download" VALUES (2,2,'국정농단 사건 등으로 유죄 확정을 받아 수감 중인 박근혜(69) 전 대통령이 특별사면·복권됐다. 2017년 3월 31일 구속된 이후 4년 9개월 만이다.',NULL,NULL,NULL);
INSERT INTO "user_data" VALUES (1,1,'samsung');
INSERT INTO "user_data" VALUES (2,1,'LG Energy Solution');
INSERT INTO "user_data" VALUES (3,1,'SK Hynix');
INSERT INTO "user_data" VALUES (4,1,'Hyundai motors');
INSERT INTO "user_data" VALUES (5,1,'ASML');
INSERT INTO "user_data" VALUES (6,1,'asml');
INSERT INTO "user" VALUES (1,'sunup','pbkdf2:sha256:260000$akIhZmj8s7esgJuS$a7aa93fd35487875831a265f430c6be6bd4c3f06bc80710320d2c35a9817367f','sunup@s-econ.kr',NULL,'samsung');
COMMIT;
