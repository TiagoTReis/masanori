<script setup>
import { ref, computed } from 'vue'
import api from '../services/api'

const emit = defineEmits([
  'lead-created',
  'cancel',
])

const initialFormState = () => ({
  name: '',
  email: '',
  phone: '',
  company: '',
  status: 'new',
  source: 'website',
})

const form = ref(initialFormState())

const loading = ref(false)
const error = ref(null)

/* =========================
   PROTEÇÃO CONTRA FECHAMENTO ACIDENTAL
========================= */

const hasUnsavedChanges = computed(() => {
  return (
    form.value.name.trim() !== '' ||
    form.value.email.trim() !== '' ||
    form.value.phone.trim() !== '' ||
    form.value.company.trim() !== ''
  )
})

const attemptClose = () => {
  if (hasUnsavedChanges.value) {
    const confirmDiscard = window.confirm(
      'Você tem dados não salvos neste formulário. Deseja realmente fechar sem cadastrar o lead?'
    )

    if (!confirmDiscard) return
  }

  cancel()
}

const formatPhone = (value) => {
  const numbers = String(value || '').replace(/\D/g, '')

  if (numbers.length <= 10) {
    return numbers
      .replace(/^(\d{2})(\d)/, '($1) $2')
      .replace(/(\d{4})(\d)/, '$1-$2')
  }

  return numbers
    .replace(/^(\d{2})(\d)/, '($1) $2')
    .replace(/(\d{5})(\d)/, '$1-$2')
}

const handlePhoneInput = (event) => {
  form.value.phone = formatPhone(event.target.value)
}

const resetForm = () => {
  form.value = initialFormState()
  error.value = null
}

const cancel = () => {
  resetForm()
  emit('cancel')
}

const submitForm = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await api.post(
      '/leads/',
      form.value
    )

    emit('lead-created', response.data)

    resetForm()

    emit('cancel')
  } catch (err) {
    error.value = 'Não foi possível cadastrar o lead.'
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div
    class="modal-overlay"
    @click.self="attemptClose"
  >
    <div class="modal">

      <div class="modal-header">
        <div>
          <h3>Novo Lead</h3>
          <p>Cadastre um novo contato no CRM.</p>
        </div>

        <button
          type="button"
          class="close-button"
          @click="attemptClose"
        >
          ×
        </button>
      </div>

      <form @submit.prevent="submitForm">

        <div class="form-group">
          <label for="name">
            Nome
          </label>

          <input
            id="name"
            v-model="form.name"
            type="text"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">
            E-mail
          </label>

          <input
            id="email"
            v-model="form.email"
            type="email"
            required
          />
        </div>

        <div class="form-row">

          <div class="form-group">
            <label for="phone">
              Telefone
            </label>

            <input
              id="phone"
              :value="form.phone"
              type="text"
              inputmode="numeric"
              maxlength="15"
              required
              @input="handlePhoneInput"
            />
          </div>

          <div class="form-group">
            <label for="company">
              Empresa
            </label>

            <input
              id="company"
              v-model="form.company"
              type="text"
              required
            />
          </div>

        </div>

        <div class="form-row">

          <div class="form-group">
            <label for="status">
              Status
            </label>

            <select
              id="status"
              v-model="form.status"
            >
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

          <div class="form-group">
            <label for="source">
              Origem
            </label>

            <select
              id="source"
              v-model="form.source"
            >
              <option value="website">
                Website
              </option>

              <option value="instagram">
                Instagram
              </option>

              <option value="linkedin">
                LinkedIn
              </option>
            </select>
          </div>

        </div>

        <p
          v-if="error"
          class="error-message"
        >
          {{ error }}
        </p>

        <div class="modal-footer">

          <button
            type="button"
            class="cancel-button"
            :disabled="loading"
            @click="cancel"
          >
            Cancelar
          </button>

          <button
            type="submit"
            class="save-button"
            :disabled="loading"
          >
            {{
              loading
                ? 'Cadastrando...'
                : 'Cadastrar Lead'
            }}
          </button>

        </div>

      </form>
    </div>
  </div>
</template>

<style scoped>
/* =========================
   OVERLAY
========================= */

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

/* =========================
   MODAL
========================= */

.modal {
  width: 100%;
  max-width: 650px;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 28px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.55);
}

/* =========================
   CABEÇALHO
========================= */

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #30363d;
}

.modal-header h3 {
  margin: 0 0 6px;
  color: #e1e2eb;
  font-size: 22px;
  font-weight: 400;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.modal-header p {
  margin: 0;
  color: #999077;
  font-size: 13px;
}

.close-button {
  border: none;
  background: transparent;
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
  color: #999077;
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #ffd700;
}

/* =========================
   CAMPOS
========================= */

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 18px;
}

.form-group label {
  color: #d0c6ab;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.form-group input,
.form-group select {
  padding: 11px 12px;
  background: #0b0e14;
  border: 1px solid #30363d;
  border-radius: 5px;
  color: #e1e2eb;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s ease;
}

.form-group input::placeholder {
  color: #666;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #ffd700;
}

.form-group select {
  cursor: pointer;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* =========================
   RODAPÉ
========================= */

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
  padding-top: 20px;
  border-top: 1px solid #30363d;
}

.cancel-button,
.save-button {
  padding: 11px 22px;
  border-radius: 999px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.6px;
  transition:
    background 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease;
}

.cancel-button {
  background: transparent;
  border: 1px solid #30363d;
  color: #d0c6ab;
}

.cancel-button:hover:not(:disabled) {
  border-color: #ffd700;
  color: #ffd700;
}

.save-button {
  background: #ffd700;
  border: 1px solid #ffd700;
  color: #15171b;
}

.save-button:hover:not(:disabled) {
  background: #e9c400;
  border-color: #e9c400;
}

.save-button:disabled,
.cancel-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* =========================
   ERRO
========================= */

.error-message {
  color: #ffb4ab;
  font-size: 13px;
  margin: 0 0 16px;
}

/* =========================
   RESPONSIVIDADE
========================= */

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .modal {
    padding: 20px;
  }
}
</style>