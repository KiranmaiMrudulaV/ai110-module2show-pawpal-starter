import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Supply, MedicalCondition, Scheduler, save_to_json, load_from_json

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# --- Session state init: load from file on first run ---
if "owner" not in st.session_state:
    saved = load_from_json()
    st.session_state.owner = saved
    st.session_state.scheduler = Scheduler(owner=saved) if saved else None

PRIORITY_COLORS = {"high": "#ff4b4b", "medium": "#ffa500", "low": "#21c354"}

def priority_badge(priority):
    color = PRIORITY_COLORS.get(priority, "#888")
    return f'<span style="background:{color};color:white;padding:2px 8px;border-radius:10px;font-size:12px">{priority.upper()}</span>'

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.title("🐾 PawPal+")
    st.caption("Smart pet care management")
    st.divider()

    # Owner setup
    st.header("👤 Owner")
    existing_name = st.session_state.owner.name if st.session_state.owner else ""
    owner_name = st.text_input("Your name", value=existing_name)
    if st.button("Create / Reset Owner", use_container_width=True):
        st.session_state.owner = Owner(name=owner_name)
        st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
        save_to_json(st.session_state.owner)
        st.success(f"Welcome, {owner_name}!")

    if not st.session_state.owner:
        st.info("Enter your name above and click Create to begin.")
        st.stop()

    owner = st.session_state.owner
    scheduler = st.session_state.scheduler

    st.divider()

    # Add pet — counter clears the form after each submission
    st.header("🐾 Add a Pet")
    if "pet_form_counter" not in st.session_state:
        st.session_state.pet_form_counter = 0

    with st.form(f"add_pet_form_{st.session_state.pet_form_counter}"):
        col1, col2 = st.columns(2)
        with col1:
            pet_name    = st.text_input("Name")
            pet_species = st.selectbox("Species", ["dog", "cat", "bird", "turtle", "rabbit", "other"])
            pet_breed   = st.text_input("Breed")
        with col2:
            pet_age      = st.number_input("Age (years)", min_value=0, max_value=50, value=1)
            pet_vet_name = st.text_input("Vet name")
            pet_vet_ph   = st.text_input("Vet phone")
        pet_breed_info = st.text_area("Breed / species notes", height=60,
                                      placeholder="e.g. Turtles carry Salmonella, need UVB light...")
        if st.form_submit_button("Add Pet", use_container_width=True):
            if pet_name:
                owner.add_pet(Pet(
                    name=pet_name, species=pet_species, breed=pet_breed,
                    age=pet_age, vet_name=pet_vet_name, vet_phone=pet_vet_ph,
                    breed_info=pet_breed_info,
                ))
                save_to_json(owner)
                st.session_state.pet_form_counter += 1
                st.rerun()
            else:
                st.warning("Please enter a pet name.")

# ── MAIN AREA ─────────────────────────────────────────────
owner    = st.session_state.owner
scheduler= st.session_state.scheduler

st.title(f"🐾 PawPal+ — {owner.name}'s Dashboard")

if not owner.pets:
    st.info("No pets yet. Add one in the sidebar to get started!")
    st.stop()

# ── TABS ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📅 Today", "🗓️ Weekly", "📆 4 Weeks", "➕ Add Task", "🐾 Pets & Supplies"]
)

# ── TAB 1: TODAY ──────────────────────────────────────────
with tab1:
    st.subheader(f"Today's Schedule — {date.today().strftime('%A, %B %d %Y')}")

    # Conflict warnings
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for c in conflicts:
            st.warning(f"Scheduling conflict: {c}")

    schedule = scheduler.get_todays_schedule()
    if schedule:
        for pet, task in schedule:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
            with col1:
                st.markdown(f"**{task.time}**")
            with col2:
                dose = f" ({task.dose_amount})" if task.dose_amount else ""
                st.markdown(f"**{task.description}**{dose} — *{pet.name}*")
            with col3:
                st.markdown(priority_badge(task.priority), unsafe_allow_html=True)
            with col4:
                btn_key = f"done_{pet.name}_{task.description}_{task.due_date}"
                if not task.completed:
                    if st.button("Mark done", key=btn_key):
                        scheduler.mark_task_complete(pet.name, task.description)
                        save_to_json(owner)
                        st.rerun()
                else:
                    st.success("Done")
    else:
        st.info("No pending tasks for today.")

    # Supply warnings across all pets
    any_supply_warning = False
    for pet in owner.pets:
        for warning in pet.check_supplies():
            st.error(f"{pet.name}: {warning}")
            any_supply_warning = True
    if not any_supply_warning and owner.pets:
        st.success("All supplies are stocked.")

# ── TAB 2: WEEKLY ─────────────────────────────────────────
with tab2:
    st.subheader("This Week's Schedule")
    weekly = scheduler.get_schedule_range(7)
    for day, tasks in weekly.items():
        label = day.strftime("%A, %b %d")
        if day == date.today():
            label += "  ← Today"
        with st.expander(label, expanded=(day == date.today())):
            if tasks:
                rows = []
                for pet, task in tasks:
                    rows.append({
                        "Time": task.time,
                        "Pet": pet.name,
                        "Task": task.description,
                        "Priority": task.priority.upper(),
                        "Status": "Done" if task.completed else "Pending",
                    })
                st.table(rows)
            else:
                st.caption("No tasks scheduled.")

# ── TAB 3: 4 WEEKS ────────────────────────────────────────
with tab3:
    st.subheader("Next 4 Weeks")
    four_weeks = scheduler.get_schedule_range(28)
    for day, tasks in four_weeks.items():
        if tasks:
            label = day.strftime("%A, %b %d")
            with st.expander(label):
                rows = [{"Time": t.time, "Pet": p.name, "Task": t.description,
                         "Priority": t.priority.upper()} for p, t in tasks]
                st.table(rows)

# ── TAB 4: ADD TASK ───────────────────────────────────────
with tab4:
    st.subheader("Schedule a New Task")
    with st.form("add_task_form"):
        col1, col2 = st.columns(2)
        with col1:
            target_pet  = st.selectbox("Pet", [p.name for p in owner.pets])
            task_desc   = st.text_input("Description", placeholder="e.g. Morning walk")
            task_time   = st.text_input("Time (HH:MM)", value="08:00")
            task_due    = st.date_input("Due date", value=date.today())
        with col2:
            task_freq   = st.selectbox("Frequency", ["once", "daily", "weekly"])
            task_pri    = st.selectbox("Priority", ["high", "medium", "low"], index=1)
            task_dose   = st.text_input("Dose amount (if medication)", placeholder="e.g. 5mg")

        if st.form_submit_button("Add Task", use_container_width=True):
            if task_desc and task_time:
                for pet in owner.pets:
                    if pet.name == target_pet:
                        pet.add_task(Task(
                            description=task_desc, time=task_time,
                            frequency=task_freq, priority=task_pri,
                            due_date=task_due, dose_amount=task_dose,
                        ))
                        save_to_json(owner)
                        st.success(f"Task '{task_desc}' added to {target_pet}!")
                        break
            else:
                st.warning("Please fill in description and time.")

    st.divider()
    st.subheader("Track a Supply")
    with st.form("add_supply_form"):
        col1, col2 = st.columns(2)
        with col1:
            sup_pet    = st.selectbox("Pet", [p.name for p in owner.pets], key="sup_pet")
            sup_name   = st.text_input("Supply name", placeholder="e.g. Kibble, Insulin")
            sup_unit   = st.text_input("Unit", placeholder="e.g. grams, ml, tablets")
        with col2:
            sup_qty    = st.number_input("Quantity bought", min_value=1.0, value=500.0)
            sup_daily  = st.number_input("Daily amount used", min_value=0.1, value=50.0)
            sup_bought = st.date_input("Date bought", value=date.today())
            sup_remind = st.number_input("Warn X days before empty", min_value=1, max_value=14, value=3)

        if st.form_submit_button("Add Supply", use_container_width=True):
            if sup_name:
                for pet in owner.pets:
                    if pet.name == sup_pet:
                        pet.add_supply(Supply(
                            name=sup_name, quantity_bought=sup_qty,
                            daily_amount=sup_daily, bought_date=sup_bought,
                            unit=sup_unit, reminder_days_before=sup_remind,
                        ))
                        save_to_json(owner)
                        st.success(f"Supply '{sup_name}' added to {sup_pet}!")
                        break

# ── TAB 5: PETS & HEALTH ──────────────────────────────────
with tab5:
    st.subheader("Pet Profiles")
    for pet in owner.pets:
        with st.expander(f"{pet.name} ({pet.species} | {pet.breed})"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Age:** {pet.age} years")
                st.markdown(f"**Vet:** {pet.vet_name or 'Not set'}")
                st.markdown(f"**Vet phone:** {pet.vet_phone or 'Not set'}")
            with col2:
                st.markdown(f"**Total tasks:** {len(pet.tasks)}")
                st.markdown(f"**Pending:** {len(pet.get_pending_tasks())}")
                st.markdown(f"**Supplies tracked:** {len(pet.supplies)}")

            if pet.breed_info:
                st.info(f"Species notes: {pet.breed_info}")

            if pet.medical_conditions:
                st.markdown("**Medical conditions:**")
                for cond in pet.medical_conditions:
                    st.markdown(f"- {cond.name} (diagnosed {cond.date_diagnosed}) — {cond.medication} {cond.dose}")

            # Add medical condition inline
            counter_key = f"med_counter_{pet.name}"
            if counter_key not in st.session_state:
                st.session_state[counter_key] = 0
            counter = st.session_state[counter_key]

            with st.form(f"med_{pet.name}_{counter}"):
                st.markdown("Add medical condition")
                c1, c2, c3 = st.columns(3)
                with c1:
                    mc_name = st.text_input("Condition")
                    mc_diag = st.date_input("Date diagnosed")
                with c2:
                    mc_med  = st.text_input("Medication")
                    mc_dose = st.text_input("Dose")
                with c3:
                    mc_notes = st.text_area("Notes", height=68)
                if st.form_submit_button("Save condition"):
                    if mc_name:
                        pet.medical_conditions.append(MedicalCondition(
                            name=mc_name, date_diagnosed=mc_diag,
                            medication=mc_med, dose=mc_dose, notes=mc_notes,
                        ))
                        save_to_json(owner)
                        st.session_state[counter_key] += 1
                        st.rerun()
