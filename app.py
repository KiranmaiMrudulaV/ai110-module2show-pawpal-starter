import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Supply, MedicalCondition, Scheduler, save_to_json, load_from_json

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# --- Session state init: load from file on first run ---
if "owner" not in st.session_state:
    saved = load_from_json()
    st.session_state.owner = saved
    st.session_state.scheduler = Scheduler(owner=saved) if saved else None

# --- Color scheme ---
PRIORITY_COLORS = {
    "high":   {"bg": "#fde8e8", "border": "#dc3545"},
    "medium": {"bg": "#fff3e0", "border": "#fd7e14"},
    "low":    {"bg": "#fffde7", "border": "#ffc107"},
}
DONE_COLORS = {"bg": "#d4edda", "border": "#28a745"}

# --- Global CSS: scrollable board rows ---
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] {
    overflow-x: auto;
    flex-wrap: nowrap !important;
    padding-bottom: 10px;
    gap: 10px;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
    min-width: 200px !important;
    flex: 0 0 auto !important;
}
.pet-row-label {
    background: #f0f2f6;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 8px;
    display: inline-block;
}
.day-label {
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)


def render_card(pet, task, scheduler, owner, key_suffix=""):
    """Render a single task card with checkbox and expandable details all in one box."""
    if task.completed:
        c = DONE_COLORS
        name_style = "text-decoration:line-through; color:#6c757d;"
        badge_html = '<span style="background:#28a745;color:white;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">DONE</span>'
    else:
        c = PRIORITY_COLORS.get(task.priority, PRIORITY_COLORS["medium"])
        name_style = ""
        badge_colors = {"high": "#dc3545", "medium": "#fd7e14", "low": "#ffc107"}
        bc = badge_colors.get(task.priority, "#888")
        badge_html = f'<span style="background:{bc};color:white;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600">{task.priority.upper()}</span>'

    with st.container(border=True):
        st.markdown(
            f'<div style="height:5px;background:{c["border"]};border-radius:4px;margin-bottom:8px;"></div>'
            f'<div style="font-weight:700;font-size:14px;{name_style}">{task.description}</div>'
            f'<div style="font-size:12px;color:#666;margin:4px 0">{task.time} &nbsp;·&nbsp; {task.frequency}</div>'
            f'{badge_html}',
            unsafe_allow_html=True
        )

        cb_key = f"cb_{pet.name}_{task.description}_{task.due_date}_{key_suffix}"
        done = st.checkbox("Done", value=task.completed, key=cb_key)
        if done and not task.completed:
            scheduler.mark_task_complete(pet.name, task.description)
            save_to_json(owner)
            st.rerun()

        with st.expander("Details"):
            st.markdown(f"**Pet:** {pet.name} ({pet.species})")
            st.markdown(f"**Priority:** {task.priority.capitalize()}")
            st.markdown(f"**Frequency:** {task.frequency.capitalize()}")
            st.markdown(f"**Due date:** {task.due_date}")
            if task.dose_amount:
                st.markdown(f"**Dose:** {task.dose_amount}")
            if pet.vet_name:
                st.markdown(f"**Vet:** {pet.vet_name}")
            if pet.vet_phone:
                st.markdown(f"**Vet phone:** {pet.vet_phone}")
            if pet.medical_conditions:
                st.markdown("**Conditions:** " + ", ".join(m.name for m in pet.medical_conditions))


# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.title("🐾 PawPal+")
    st.caption("Smart pet care management")
    st.divider()

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

    owner    = st.session_state.owner
    scheduler= st.session_state.scheduler

    st.divider()

    st.header("🐾 Add a Pet")
    if "pet_form_counter" not in st.session_state:
        st.session_state.pet_form_counter = 0

    with st.form(f"add_pet_form_{st.session_state.pet_form_counter}"):
        col1, col2 = st.columns(2)
        with col1:
            pet_name     = st.text_input("Name")
            pet_species  = st.selectbox("Species", ["dog", "cat", "bird", "turtle", "rabbit", "other"])
            pet_breed    = st.text_input("Breed")
        with col2:
            pet_age      = st.number_input("Age (years)", min_value=0, max_value=50, value=1)
            pet_vet_name = st.text_input("Vet name")
            pet_vet_ph   = st.text_input("Vet phone")
        pet_breed_info = st.text_area("Breed / species notes", height=60,
                                      placeholder="e.g. Turtles need UVB light...")
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

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📅 Today Board", "🗓️ Weekly Board", "📆 4-Week List", "➕ Add Task / Supply", "🐾 Pets & Health"]
)

# ── TAB 1: TODAY BOARD ────────────────────────────────────
with tab1:
    st.subheader(f"Today — {date.today().strftime('%A, %B %d %Y')}")

    conflicts = scheduler.detect_conflicts()
    for c in conflicts:
        st.warning(f"Scheduling conflict: {c}")
    for pet in owner.pets:
        for w in pet.check_supplies():
            st.error(f"{pet.name}: {w}")

    st.divider()
    today = date.today()

    for pet in owner.pets:
        pending = sorted(
            [t for t in pet.tasks if t.due_date == today and not t.completed],
            key=lambda t: t.time
        )
        done = sorted(
            [t for t in pet.tasks if t.due_date == today and t.completed],
            key=lambda t: t.time
        )
        tasks_today = pending + done  # pending cards first, done cards at end

        pending_count = len(pending)
        st.markdown(
            f'<div class="pet-row-label">🐾 {pet.name}'
            f'<span style="font-weight:400;font-size:13px;color:#666"> &nbsp;{pet.species}'
            f' &nbsp;·&nbsp; {pending_count} pending</span></div>',
            unsafe_allow_html=True
        )

        if tasks_today:
            cols = st.columns(len(tasks_today))
            for i, task in enumerate(tasks_today):
                with cols[i]:
                    render_card(pet, task, scheduler, owner, key_suffix=f"today_{i}")
        else:
            st.caption("No tasks for today.")

        st.divider()

# ── TAB 2: WEEKLY BOARD ───────────────────────────────────
with tab2:
    st.subheader("Weekly Board")
    weekly = scheduler.get_schedule_range(7)

    for day, tasks in weekly.items():
        is_today = day == date.today()
        bg = "#e3f2fd" if is_today else "#f8f9fa"
        label = ("📍 " if is_today else "") + day.strftime("%A, %b %d")
        st.markdown(
            f'<div class="day-label" style="background:{bg}">{label}'
            f'<span style="font-weight:400;font-size:13px;color:#666"> &nbsp;·&nbsp; {len(tasks)} tasks</span></div>',
            unsafe_allow_html=True
        )

        if tasks:
            pending = sorted([(p, t) for p, t in tasks if not t.completed], key=lambda x: x[1].time)
            done    = sorted([(p, t) for p, t in tasks if t.completed],     key=lambda x: x[1].time)
            ordered = pending + done

            cols = st.columns(len(ordered))
            for i, (pet, task) in enumerate(ordered):
                with cols[i]:
                    st.caption(f"🐾 {pet.name}")
                    render_card(pet, task, scheduler, owner, key_suffix=f"week_{day}_{i}")
        else:
            st.caption("Nothing scheduled.")

        st.divider()

# ── TAB 3: 4-WEEK LIST ────────────────────────────────────
with tab3:
    st.subheader("Next 4 Weeks — Task List")
    four_weeks = scheduler.get_schedule_range(28)
    any_tasks = False
    for day, tasks in four_weeks.items():
        if tasks:
            any_tasks = True
            label = day.strftime("%A, %b %d")
            if day == date.today():
                label = "Today — " + label
            with st.expander(f"{label}  ({len(tasks)} tasks)"):
                rows = [{
                    "Time": t.time,
                    "Pet": p.name,
                    "Task": t.description,
                    "Priority": t.priority.upper(),
                    "Frequency": t.frequency,
                    "Status": "Done" if t.completed else "Pending",
                } for p, t in tasks]
                st.table(rows)
    if not any_tasks:
        st.info("No tasks in the next 4 weeks.")

# ── TAB 4: ADD TASK / SUPPLY ──────────────────────────────
with tab4:
    st.subheader("Schedule a New Task")
    with st.form("add_task_form"):
        col1, col2 = st.columns(2)
        with col1:
            target_pet = st.selectbox("Pet", [p.name for p in owner.pets])
            task_desc  = st.text_input("Description", placeholder="e.g. Morning walk")
            task_time  = st.text_input("Time (HH:MM)", value="08:00")
            task_due   = st.date_input("Due date", value=date.today())
        with col2:
            task_freq  = st.selectbox("Frequency", ["once", "daily", "weekly"])
            task_pri   = st.selectbox("Priority", ["high", "medium", "low"], index=1)
            task_dose  = st.text_input("Dose (if medication)", placeholder="e.g. 5mg")
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
                    st.markdown(
                        f"- **{cond.name}** (diagnosed {cond.date_diagnosed})"
                        f" — {cond.medication} {cond.dose}"
                        + (f" · {cond.notes}" if cond.notes else "")
                    )

            counter_key = f"med_counter_{pet.name}"
            if counter_key not in st.session_state:
                st.session_state[counter_key] = 0

            with st.form(f"med_{pet.name}_{st.session_state[counter_key]}"):
                st.markdown("**Add medical condition**")
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
