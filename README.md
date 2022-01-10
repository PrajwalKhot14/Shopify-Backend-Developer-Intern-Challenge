# Shopify-Backend-Developer-Intern-Challenge
1. PostgreSQL needs to be installed to run
   Credentials: username: postgres
                password: 9663168172
                dbname: shopify
2. Create Table using: 
   ```
   CREATE TABLE IF NOT EXISTS public.py_users
   (
    id character varying COLLATE pg_catalog."default" NOT NULL,
    username character varying COLLATE pg_catalog."default",
    password character varying COLLATE pg_catalog."default",
    first_name character varying COLLATE pg_catalog."default",
    last_name character varying COLLATE pg_catalog."default",
    gender character(1) COLLATE pg_catalog."default",
    create_at character varying COLLATE pg_catalog."default",
    status character(1) COLLATE pg_catalog."default",
    CONSTRAINT py_users_pkey PRIMARY KEY (id)
   )

   TABLESPACE pg_default;

   ALTER TABLE IF EXISTS public.py_users
      OWNER to postgres;
   ```
4. I have attached requirements.text, install the required packages using the following code before running main.py
   ```
   pip install -r requirements.txt
   ```
