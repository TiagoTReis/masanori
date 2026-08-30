
<script setup>
import { ref } from 'vue'
import api from '../services/api'

const props = defineProps({
  lead: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['close'])

const interactionType = ref('note')
const interactionDescription = ref('')
const saving = ref(false)
const error = ref(null)

const addInteraction = async () => {
  if (!interactionDescription.value.trim()) {
    return
  }

  saving.value = true
  error.value = null

  try {
    const response = await api.post(
      `/leads/${props.lead._id}/interactions/`,
      {
        type: interactionType.value,
        description: interactionDescription.value.trim(),
      }
    )

    props.lead.interactions = response.data.interactions

    interactionDescription.value = ''
  } catch (err) {
    error.value = 'Não foi possível adicionar a interação.'
    console.error(err)
  } finally {
    saving.value = false
  }
}

const formatPhone = (phone) => {
  if (!phone) return ''

  const numbers = String(phone).replace(/\D/g, '')

  if (numbers.length === 11) {
    return numbers.replace(
      /^(\d{2})(\d{5})(\d{4})$/,
      '($1) $2-$3'
    )
  }

  if (numbers.length === 10) {
    return numbers.replace(
      /^(\d{2})(\d{4})(\d{4})$/,
      '($1) $2-$3'
    )
  }

  return phone
}

const formatDate = (date) => {
  if (!date) return ''

  return new Date(date).toLocaleString('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}

const getInteractionLabel = (type) => {
  const labels = {
    created: 'Lead cadastrado',
    note: 'Observação',
    call: 'Ligação',
    email: 'E-mail',
    meeting: 'Reunião',
  }

  return labels[type] || type
}
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal">

      <!-- CABEÇALHO -->
      <div class="modal-header">
        <div>
          <h2>{{ lead.name }}</h2>
          <p>{{ lead.company }}</p>
        </div>

        <button
          type="button"
          class="close-button"
          @click="emit('close')"
        >
          ×
        </button>
      </div>

      <!-- DADOS DO LEAD -->
      <div class="lead-info">
        <div>
          <span>E-mail</span>
          <strong>{{ lead.email }}</strong>
        </div>

        <div>
          <span>Telefone</span>
          <strong>{{ formatPhone(lead.phone) }}</strong>
        </div>

        <div>
          <span>Status</span>
          <strong>{{ lead.status }}</strong>
        </div>

        <div>
          <span>Origem</span>
          <strong>{{ lead.source }}</strong>
        </div>
      </div>

      <!-- TIMELINE -->
      <div class="timeline-section">
        <h3>Timeline de interações</h3>

        <div
          v-if="!lead.interactions || lead.interactions.length === 0"
          class="empty-timeline"
        >
          Nenhuma interação registrada.
        </div>

        <div
          v-else
          class="timeline"
        >
          <div
            v-for="(interaction, index) in [...lead.interactions].reverse()"
            :key="`${interaction.created_at}-${index}`"
            class="timeline-item"
          >
            <div class="timeline-marker"></div>

            <div class="timeline-content">
              <div class="timeline-top">
                <strong>
                  {{ getInteractionLabel(interaction.type) }}
                </strong>

                <span>
                  {{ formatDate(interaction.created_at) }}
                </span>
              </div>

              <p>
                {{ interaction.description }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- NOVA INTERAÇÃO -->
      <div class="interaction-form">
        <h3>Adicionar interação</h3>

        <div class="form-row">
          <select v-model="interactionType">
            <option value="note">
              Observação
            </option>

            <option value="call">
              Ligação
            </option>

            <option value="email">
              E-mail
            </option>

            <option value="meeting">
              Reunião
            </option>
          </select>

          <textarea
            v-model="interactionDescription"
            placeholder="Descreva a interação..."
            rows="3"
          ></textarea>
        </div>

        <p
          v-if="error"
          class="error-message"
        >
          {{ error }}
        </p>

        <button
          type="button"
          class="save-button"
          :disabled="saving || !interactionDescription.trim()"
          @click="addInteraction"
        >
          {{ saving ? 'Salvando...' : 'Adicionar interação' }}
        </button>
      </div>

    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(0, 0, 0, 0.7);
}

.modal {
  width: min(720px, 100%);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

.timeline {
  position: relative;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 24px;
  border-bottom: 1px solid #30363d;
}

.modal-header h2 {
  margin: 0 0 5px;
  color: #e1e2eb;
  font-size: 22px;
  font-weight: 500;
}

.modal-header p {
  margin: 0;
  color: #999077;
  font-size: 13px;
}

.close-button {
  border: none;
  background: transparent;
  color: #999077;
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
}

.close-button:hover {
  color: #ffd700;
}

.lead-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 20px 24px;
  border-bottom: 1px solid #30363d;
}

.lead-info div {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.lead-info span {
  color: #999077;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.lead-info strong {
  color: #d0c6ab;
  font-size: 13px;
  font-weight: 400;
}

.timeline-section,
.interaction-form {
  padding: 24px;
}

.timeline-section {
  border-bottom: 1px solid #30363d;
  min-height: 0;
  overflow-y: auto;
  flex: 1;
}

.timeline-section h3,
.interaction-form h3 {
  margin: 0 0 20px;
  color: #e1e2eb;
  font-size: 15px;
  font-weight: 500;
}

.timeline {
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 8px;
  bottom: 8px;
  left: 5px;
  width: 1px;
  background: #30363d;
}

.timeline-item {
  position: relative;
  display: flex;
  gap: 16px;
  padding-bottom: 22px;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-marker {
  position: relative;
  z-index: 1;
  flex-shrink: 0;
  width: 11px;
  height: 11px;
  margin-top: 4px;
  border: 2px solid #ffd700;
  border-radius: 50%;
  background: #161b22;
}

.timeline-content {
  flex: 1;
}

.timeline-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 6px;
}

.timeline-top strong {
  color: #d0c6ab;
  font-size: 13px;
}

.timeline-top span {
  color: #777;
  font-size: 11px;
  white-space: nowrap;
}

.timeline-content p {
  margin: 0;
  color: #999077;
  font-size: 13px;
  line-height: 1.5;
}

.empty-timeline {
  padding: 20px;
  border: 1px dashed #30363d;
  color: #777;
  text-align: center;
  font-size: 13px;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.form-row select,
.form-row textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 11px 12px;
  background: #0b0e14;
  border: 1px solid #30363d;
  border-radius: 5px;
  color: #e1e2eb;
  outline: none;
  font-size: 12px;
}

.form-row select:focus,
.form-row textarea:focus {
  border-color: #ffd700;
}

.form-row textarea {
  resize: vertical;
  font-family: inherit;
}

.save-button {
  margin-top: 14px;
  padding: 10px 16px;
  border: 1px solid #ffd700;
  border-radius: 5px;
  background: #ffd700;
  color: #15171b;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.save-button:hover:not(:disabled) {
  background: #e6c200;
}

.save-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  margin: 10px 0 0;
  color: #ffb4ab;
  font-size: 12px;
}

@media (max-width: 600px) {
  .modal-overlay {
    padding: 12px;
  }

  .lead-info {
    grid-template-columns: 1fr;
  }

  .timeline-top {
    align-items: flex-start;
    flex-direction: column;
    gap: 4px;
  }
}
</style>
