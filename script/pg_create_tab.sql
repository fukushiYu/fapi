/*
cmdinfo
*/
CREATE TABLE public.cmdinfo (
    id varchar(128) NOT NULL,
    "content" varchar(2048) NULL,
    create_time timestamp(0) NULL,
    status varchar(16) NULL,
    cnt int NULL,
    update_time timestamp(0) NULL
);
CREATE INDEX cmdinfo_id_idx ON public.cmdinfo (id);
CREATE INDEX cmdinfo_status_idx ON public.cmdinfo (status,create_time);

ALTER TABLE public.cmdinfo ALTER COLUMN create_time SET DEFAULT current_timestamp;
ALTER TABLE public.cmdinfo ALTER COLUMN update_time SET DEFAULT current_timestamp;

/* now, now+10秒
select current_timestamp,current_timestamp+10*'1 second'::interval; 
*/