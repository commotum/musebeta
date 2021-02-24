import * as React from 'react'
import { storiesOf } from '@storybook/react'
import { action } from '@storybook/addon-actions'
import { Form, Formik } from 'formik'

import { FileInput } from '../components/FileInput'

storiesOf('components/FileInput', module).add('default', () => (
  <Formik
    initialValues={{ name: '' }}
    validate={() => ({ name: 'this is an error' })}
    onSubmit={({ name }) => {
      action('onSubmit')(name)
    }}
  >
    <Form>
      <FileInput label="Label name" name="name" />
    </Form>
  </Formik>
))
