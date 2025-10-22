--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Debian 16.9-1.pgdg120+1)
-- Dumped by pg_dump version 16.9 (Debian 16.9-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activities; Type: TABLE; Schema: public; Owner: organization_user
--

CREATE TABLE public.activities (
    id integer NOT NULL,
    name character varying(155) NOT NULL,
    level integer NOT NULL,
    parent_id integer,
    is_active boolean NOT NULL
);


ALTER TABLE public.activities OWNER TO organization_user;

--
-- Name: activities_id_seq; Type: SEQUENCE; Schema: public; Owner: organization_user
--

CREATE SEQUENCE public.activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activities_id_seq OWNER TO organization_user;

--
-- Name: activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: organization_user
--

ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: organization_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO organization_user;

--
-- Name: buildings; Type: TABLE; Schema: public; Owner: organization_user
--

CREATE TABLE public.buildings (
    id integer NOT NULL,
    address character varying(155) NOT NULL,
    latitude numeric(9,6) NOT NULL,
    longitude numeric(9,6) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.buildings OWNER TO organization_user;

--
-- Name: buildings_id_seq; Type: SEQUENCE; Schema: public; Owner: organization_user
--

CREATE SEQUENCE public.buildings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.buildings_id_seq OWNER TO organization_user;

--
-- Name: buildings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: organization_user
--

ALTER SEQUENCE public.buildings_id_seq OWNED BY public.buildings.id;


--
-- Name: organization_activities; Type: TABLE; Schema: public; Owner: organization_user
--

CREATE TABLE public.organization_activities (
    organization_id integer NOT NULL,
    activity_id integer NOT NULL
);


ALTER TABLE public.organization_activities OWNER TO organization_user;

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: organization_user
--

CREATE TABLE public.organizations (
    id integer NOT NULL,
    name character varying(155) NOT NULL,
    building_id integer NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public.organizations OWNER TO organization_user;

--
-- Name: organizations_id_seq; Type: SEQUENCE; Schema: public; Owner: organization_user
--

CREATE SEQUENCE public.organizations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organizations_id_seq OWNER TO organization_user;

--
-- Name: organizations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: organization_user
--

ALTER SEQUENCE public.organizations_id_seq OWNED BY public.organizations.id;


--
-- Name: phones; Type: TABLE; Schema: public; Owner: organization_user
--

CREATE TABLE public.phones (
    id integer NOT NULL,
    phone_number character varying(16) NOT NULL,
    organization_id integer,
    is_active boolean NOT NULL
);


ALTER TABLE public.phones OWNER TO organization_user;

--
-- Name: phones_id_seq; Type: SEQUENCE; Schema: public; Owner: organization_user
--

CREATE SEQUENCE public.phones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.phones_id_seq OWNER TO organization_user;

--
-- Name: phones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: organization_user
--

ALTER SEQUENCE public.phones_id_seq OWNED BY public.phones.id;


--
-- Name: activities id; Type: DEFAULT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);


--
-- Name: buildings id; Type: DEFAULT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.buildings ALTER COLUMN id SET DEFAULT nextval('public.buildings_id_seq'::regclass);


--
-- Name: organizations id; Type: DEFAULT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.organizations ALTER COLUMN id SET DEFAULT nextval('public.organizations_id_seq'::regclass);


--
-- Name: phones id; Type: DEFAULT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.phones ALTER COLUMN id SET DEFAULT nextval('public.phones_id_seq'::regclass);


--
-- Data for Name: activities; Type: TABLE DATA; Schema: public; Owner: organization_user
--

COPY public.activities (id, name, level, parent_id, is_active) FROM stdin;
1	Еда	1	\N	t
2	Налоги	1	\N	t
3	Гос услуги	1	\N	t
4	Фармацевтика	1	\N	t
6	металы	1	\N	t
5	роботизированная техника	1	6	t
7	добыча металов	1	6	t
8	Оружие	1	\N	t
9	продажа оружия и средств защиты	1	8	t
10	Медицинское оборудование, медтехника	1	6	t
11	Кофейня кафе	1	1	t
12	Столовая кафе	1	1	t
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: organization_user
--

COPY public.alembic_version (version_num) FROM stdin;
5af0ee4e4b96
\.


--
-- Data for Name: buildings; Type: TABLE DATA; Schema: public; Owner: organization_user
--

COPY public.buildings (id, address, latitude, longitude, is_active) FROM stdin;
1	moskow oleinya 23	12.755800	38.617300	t
2	Петроверигский переулок, 6-8-10с2	55.756218	37.637791	t
3	Волгоградский проспект, 42к24, Москва	55.706097	37.720654	t
4	Волгоградский проспект, 42к5, Москва	55.710124	37.718253	t
5	Волгоградский проспект, 42к1, Москва	55.708302	37.726210	t
\.


--
-- Data for Name: organization_activities; Type: TABLE DATA; Schema: public; Owner: organization_user
--

COPY public.organization_activities (organization_id, activity_id) FROM stdin;
1	1
2	2
3	3
5	3
6	2
7	4
8	6
8	5
8	7
9	4
10	9
11	1
12	10
13	11
14	12
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: organization_user
--

COPY public.organizations (id, name, building_id, is_active) FROM stdin;
1	Столовая училища	2	t
2	Инспекция Федеральной налоговой службы России № 9 по г. Москве	2	t
3	Центр госуслуг района Люблино	2	f
5	Центр гос услуг района Люблино	3	t
6	Инспекция Федеральной налоговой службы России № 23 по г. Москве	3	t
7	ОнкоТаргет	3	t
8	Технорэд	3	t
9	Спутник Технополис	3	t
10	Спорт Виапон Кастом	3	t
11	Zar-Pizza	4	t
12	Тюменский завод медицинского оборудования и инструментов	4	t
13	Fro  	5	t
14	Столовая	5	t
\.


--
-- Data for Name: phones; Type: TABLE DATA; Schema: public; Owner: organization_user
--

COPY public.phones (id, phone_number, organization_id, is_active) FROM stdin;
1	89708682593	1	t
2	89709623598	1	t
3	89749466591	2	t
4	89741464561	2	t
5	8347414589	3	t
6	8341314569	3	t
8	8391834569	5	t
9	8996824169	5	t
10	8998872139	6	t
11	8991772152	6	t
12	8958719156	7	t
13	8958129353	8	t
14	8952029353	8	t
15	8952081753	8	t
16	8952777743	9	t
17	8934755743	10	t
18	8999712791	10	t
19	8928814596	11	t
20	8928211596	12	t
21	8948711526	12	t
22	8991866726	13	t
23	8926899126	14	t
24	8923899426	14	t
\.


--
-- Name: activities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: organization_user
--

SELECT pg_catalog.setval('public.activities_id_seq', 12, true);


--
-- Name: buildings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: organization_user
--

SELECT pg_catalog.setval('public.buildings_id_seq', 5, true);


--
-- Name: organizations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: organization_user
--

SELECT pg_catalog.setval('public.organizations_id_seq', 14, true);


--
-- Name: phones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: organization_user
--

SELECT pg_catalog.setval('public.phones_id_seq', 24, true);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: buildings buildings_address_key; Type: CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_address_key UNIQUE (address);


--
-- Name: buildings buildings_pkey; Type: CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_pkey PRIMARY KEY (id);


--
-- Name: organization_activities organization_activities_pkey; Type: CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.organization_activities
    ADD CONSTRAINT organization_activities_pkey PRIMARY KEY (organization_id, activity_id);


--
-- Name: organizations organizations_name_key; Type: CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_name_key UNIQUE (name);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);


--
-- Name: phones phones_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_phone_number_key UNIQUE (phone_number);


--
-- Name: phones phones_pkey; Type: CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_pkey PRIMARY KEY (id);


--
-- Name: activities activities_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.activities(id);


--
-- Name: organization_activities organization_activities_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.organization_activities
    ADD CONSTRAINT organization_activities_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id);


--
-- Name: organization_activities organization_activities_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.organization_activities
    ADD CONSTRAINT organization_activities_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: organizations organizations_building_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.buildings(id);


--
-- Name: phones phones_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: organization_user
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- PostgreSQL database dump complete
--

