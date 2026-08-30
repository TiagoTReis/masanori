<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import api from '../services/api'
import LeadItem from './LeadItem.vue'
import LeadEdit from './LeadEdit.vue'
import LeadDetails from './LeadDetails.vue'
import Pagination from './Pagination.vue'

const emit = defineEmits(['leads-loaded'])

const leads = ref([])
const loading = ref(true)
const error = ref(null)

const editingLead = ref(null)
const selectedLead = ref(null)
const search = ref('')
const statusFilter = ref('all')

/* =========================
   PAGINAÇÃO
========================= */

const currentPage = ref(1)
const itemsPerPage = ref(10)

const addLead = (lead) => {
  leads.value.unshift(lead)
  emit('leads-loaded', leads.value)
}

const deleteLead = async (id) => {
  try {
    await api.delete(`/leads/${id}/`)

    leads.value = leads.value.filter(
      (lead) => lead._id !== id
    )

    emit('leads-loaded', leads.value)
  } catch (err) {
    error.value = 'Não foi possível excluir o lead.'
    console.error(err)
  }
}

const editLead = (lead) => {
  editingLead.value = lead
}

const cancelEdit = () => {
  editingLead.value = null
}

const openLeadDetails = (lead) => {
  selectedLead.value = lead
}

const closeLeadDetails = () => {
  selectedLead.value = null
}

const updateLead = async ({ id, data }) => {
  try {
    const response = await api.patch(
      `/leads/${id}/`,
      data
    )

    const index = leads.value.findIndex(
      (item) => item._id === id
    )

    if (index !== -1) {
      leads.value[index] = response.data
    }

    emit('leads-loaded', leads.value)

    editingLead.value = null

    console.log('Lead atualizado:', response.data)
  } catch (err) {
    error.value = 'Não foi possível atualizar o lead.'
    console.error('Erro ao atualizar lead:', err)
  }
}

/* =========================
   BUSCA E FILTRO
========================= */

const filteredLeads = computed(() => {
  const term = search.value.toLowerCase().trim()

  return leads.value.filter((lead) => {
    const matchesSearch =
      lead.name.toLowerCase().includes(term) ||
      lead.email.toLowerCase().includes(term) ||
      lead.company.toLowerCase().includes(term)

    const matchesStatus =
      statusFilter.value === 'all' ||
      lead.status === statusFilter.value

    return matchesSearch && matchesStatus
  })
})

/* =========================
   PAGINAÇÃO DA LISTA FILTRADA
========================= */

const totalPages = computed(() => {
  return Math.max(
    1,
    Math.ceil(filteredLeads.value.length / itemsPerPage.value)
  )
})

const paginatedLeads = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value

  return filteredLeads.value.slice(start, end)
})

// Sempre que a busca ou o filtro de status mudar, volta pra página 1
watch([search, statusFilter], () => {
  currentPage.value = 1
})

/* =========================
   CARREGAR LEADS
========================= */

onMounted(async () => {
  try {
    const response = await api.get('/leads/')

    leads.value = response.data

    emit('leads-loaded', leads.value)
  } catch (err) {
    error.value = 'Não foi possível carregar os leads.'
    console.error(err)
  } finally {
    loading.value = false
  }
})

defineExpose({
  addLead,
})
</script>

<template>
  <section class="card">

    <!-- CABEÇALHO -->
    <div class="list-header">

      <div>
        <h3>LEADS RECENTES</h3>
        <p>Contatos e oportunidades cadastrados no CRM.</p>
      </div>

    </div>

    <!-- BUSCA E FILTRO -->
    <div
      v-if="!loading && !error"
      class="filters"
    >

      <div class="search-wrapper">
        <span class="search-icon">⌕</span>

        <input
          v-model="search"
          type="text"
          placeholder="BUSCAR POR NOME, E-MAIL OU EMPRESA..."
          class="search-input"
        />
      </div>

      <select
        v-model="statusFilter"
        class="status-filter"
      >
        <option value="all">
          Todos os status
        </option>

        <option value="new">
          Novo
        </option>

        <option value="contacted">
          Contatado
        </option>

        <option value="qualified">
          Qualificado
        </option>
      </select>

    </div>

    <!-- LOADING -->
    <div
      v-if="loading"
      class="message"
    >
      Carregando leads...
    </div>

    <!-- ERRO -->
    <div
      v-else-if="error"
      class="message error"
    >
      {{ error }}
    </div>

    <!-- LISTA -->
    <div
      v-else
      class="table-container"
    >

      <div
        v-if="filteredLeads.length === 0"
        class="message"
      >
        Nenhum lead encontrado.
      </div>

      <table v-else>

        <thead>
          <tr>
            <th>Nome</th>
            <th>E-mail</th>
            <th>Telefone</th>
            <th>Empresa</th>
            <th>Status</th>
            <th>Origem</th>
            <th class="actions-header">Ações</th>
          </tr>
        </thead>

        <tbody>

          <LeadItem
            v-for="lead in paginatedLeads"
            :key="lead._id"
            :lead="lead"
            @delete="deleteLead(lead._id)"
            @edit="editLead(lead)"
            @details="openLeadDetails(lead)"
          />

        </tbody>

      </table>

    </div>

    <!-- PAGINAÇÃO -->
    <Pagination
      v-if="!loading && !error"
      :current-page="currentPage"
      :total-pages="totalPages"
      :total-items="filteredLeads.length"
      :items-per-page="itemsPerPage"
      @change-page="currentPage = $event"
    />

    <!-- MODAL DE EDIÇÃO -->
    <LeadEdit
      v-if="editingLead"
      :lead="editingLead"
      @cancel="cancelEdit"
      @update="updateLead"
    />

    <LeadDetails
      v-if="selectedLead"
      :lead="selectedLead"
      @close="closeLeadDetails"
    />

  </section>
</template>

<style scoped>

/* =========================
   CARD PRINCIPAL
========================= */

.card {
  width: 100%;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  overflow: hidden;
}

/* =========================
   CABEÇALHO
========================= */

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: #191c22;
  border-bottom: 1px solid #30363d;
}

.list-header h3 {
  margin: 0 0 5px;
  color: #e1e2eb;
  font-size: 20px;
  font-weight: 400;
  letter-spacing: 1.5px;
}

.list-header p {
  margin: 0;
  color: #999077;
  font-size: 13px;
}

/* =========================
   FILTROS
========================= */

.filters {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 24px;
  background: #161b22;
  border-bottom: 1px solid #30363d;
}

.search-wrapper {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #999077;
  font-size: 20px;
  pointer-events: none;
}

.search-input {
  width: 100%;
  box-sizing: border-box;
  padding: 11px 12px 11px 38px;
  background: #0b0e14;
  border: 1px solid #30363d;
  border-radius: 5px;
  color: #e1e2eb;
  outline: none;
  font-size: 12px;
  letter-spacing: 0.8px;
  transition: border-color 0.2s ease;
}

.search-input::placeholder {
  color: #777;
}

.search-input:focus {
  border-color: #ffd700;
}

/* =========================
   FILTRO DE STATUS
========================= */

.status-filter {
  width: 180px;
  padding: 11px 12px;
  background: #0b0e14;
  border: 1px solid #30363d;
  border-radius: 5px;
  color: #e1e2eb;
  outline: none;
  font-size: 12px;
  cursor: pointer;
}

.status-filter:focus {
  border-color: #ffd700;
}

/* =========================
   TABELA
========================= */

.table-container {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

thead {
  background: #0b0e14;
}

th {
  padding: 14px 16px;
  border-bottom: 1px solid #30363d;
  color: #999077;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  white-space: nowrap;
}

.actions-header {
  text-align: right;
}

/* =========================
   LINHAS
========================= */

:deep(tbody tr) {
  border-bottom: 1px solid #30363d;
  transition: background 0.2s ease;
}

:deep(tbody tr:last-child) {
  border-bottom: none;
}

:deep(tbody tr:hover) {
  background: #1d2026;
}

:deep(td) {
  padding: 16px;
  color: #d0c6ab;
  font-size: 13px;
  white-space: nowrap;
}

/* =========================
   STATUS
========================= */

:deep(.status) {
  display: inline-flex;
  align-items: center;
  padding: 5px 9px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

/* =========================
   MENSAGENS
========================= */

.message {
  padding: 40px 24px;
  text-align: center;
  color: #999077;
  font-size: 14px;
}

.message.error {
  color: #ffb4ab;
}

/* =========================
   RESPONSIVIDADE
========================= */

@media (max-width: 800px) {

  .filters {
    flex-direction: column;
    align-items: stretch;
  }

  .status-filter {
    width: 100%;
  }

}

@media (max-width: 600px) {

  .list-header {
    padding: 18px 16px;
  }

  .filters {
    padding: 14px 16px;
  }

  th,
  :deep(td) {
    padding: 12px;
  }

}
</style>