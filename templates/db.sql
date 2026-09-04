create table public.students (
  id bigint generated always as identity primary key,
  name text not null,
  email text not null unique,
  age integer,
  course text
);

alter table public.students enable row level security;

create policy "allow full access" on public.students
  for all using (true) with check (true);