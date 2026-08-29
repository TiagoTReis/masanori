<script setup>
import { computed } from 'vue'

const props = defineProps({
  leads: {
    type: Array,
    default: () => [],
  },
})

const totalLeads = computed(() => {
  return props.leads.length
})

const newLeads = computed(() => {
  return props.leads.filter(
    (lead) => lead.status === 'new'
  ).length
})

const contactedLeads = computed(() => {
  return props.leads.filter(
    (lead) => lead.status === 'contacted'
  ).length
})

const qualifiedLeads = computed(() => {
  return props.leads.filter(
    (lead) => lead.status === 'qualified'
  ).length
})
</script>

<template>
  <section class="dashboard">

    <div class="dashboard-header">
      <div>
        <h2>Dashboard</h2>
        <p>Visão geral dos seus leads.</p>
      </div>
    </div>

    <div class="stats">

      <!-- TOTAL -->
      <div class="stat-card stat-total">
        <span class="stat-label">
          Total de Leads
        </span>

        <strong class="stat-value">
          {{ totalLeads }}
        </strong>
      </div>

      <!-- NOVOS -->
      <div class="stat-card stat-new">
        <span class="stat-label">
          Novos
        </span>

        <strong class="stat-value">
          {{ newLeads }}
        </strong>
      </div>

      <!-- CONTATADOS -->
      <div class="stat-card stat-contacted">
        <span class="stat-label">
          Contatados
        </span>

        <strong class="stat-value">
          {{ contactedLeads }}
        </strong>
      </div>

      <!-- QUALIFICADOS -->
      <div class="stat-card stat-qualified">
        <span class="stat-label">
          Qualificados
        </span>

        <strong class="stat-value">
          {{ qualifiedLeads }}
        </strong>
      </div>

    </div>

  </section>
</template>

<style scoped>
/* =========================
   DASHBOARD
========================= */

.dashboard {
  margin-bottom: 24px;
}

.dashboard-header {
  margin-bottom: 20px;
}

.dashboard-header h2 {
  margin: 0 0 6px;
}

.dashboard-header p {
  margin: 0;
  color: #6b7280;
}

/* =========================
   CARDS
========================= */

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  position: relative;
  padding: 24px;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 16px;
  overflow: hidden;
  box-sizing: border-box;
  transition: border-color 0.2s ease;
}



/* =========================
   CORES DOS CARDS
========================= */

/* TOTAL */

.stat-total {
  border-top: 3px solid #dee2ec !important;
}

.stat-total .stat-label,
.stat-total .stat-value {
  color: #dee2ec !important;
}

.stat-total:hover {
  border-color: #dee2ec;
}

/* NOVOS */

.stat-new {
  border-top: 3px solid #89d0ed !important;
}

.stat-new .stat-label,
.stat-new .stat-value {
  color: #89d0ed !important;
}

.stat-new:hover {
  border-color: #89d0ed;
}

/* CONTATADOS */

.stat-contacted {
  border-top: 3px solid #ffd700 !important;
}

.stat-contacted .stat-label,
.stat-contacted .stat-value {
  color: #ffd700 !important;
}

.stat-contacted:hover {
  border-color: #ffd700;
}

/* QUALIFICADOS */

.stat-qualified {
  border-top: 3px solid #4ade80 !important;
}

.stat-qualified .stat-label,
.stat-qualified .stat-value {
  color: #4ade80 !important;
}

.stat-qualified:hover {
  border-color: #4ade80;
}

/* =========================
   LABEL
========================= */

.stat-label {
  display: block;
  margin-bottom: 10px;
  color: #6b7280;
  font-size: 14px;
}

/* =========================
   NÚMERO
========================= */

.stat-value {
  display: block;
  font-size: 30px;
  font-weight: 700;
}

/* =========================
   RESPONSIVIDADE
========================= */

@media (max-width: 800px) {
  .stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .stats {
    grid-template-columns: 1fr;
  }
}
</style>