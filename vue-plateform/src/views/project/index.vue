<template>
<div class="app-container">
  <!-- 搜索表单 -->
    <el-form
      ref="queryParams"
      :model="queryParams"
      size="small"
      :inline="true"
    >
      <el-form-item>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增</el-button>
        <!-- <el-button type="success" icon="el-icon-edit" :disabled="single" @click="handleUpdate">修改</el-button>
        <el-button type="danger" icon="el-icon-delete" :disabled="multiple" @click="handleDelete">删除</el-button> -->
      </el-form-item>
      <el-form-item prop="project_name">
        <el-input
          v-model="queryParams.project_name"
          placeholder="项目名称"
          clearable
          style="width: 240px"
          @keyup.enter.native="showProject"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="showProject">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 列表数据 -->
    <el-table v-loading="loading"
              :data="projectList"
              border             
    >
      <el-table-column prop="prj_name" label="项目名称" min-width="80">
      <template slot-scope="scope"> {{ scope.row.fields.prj_name }} </template>
      </el-table-column>
      <el-table-column prop="version" label="项目版本" min-width="80">
      <template slot-scope="scope"> {{ scope.row.fields.version }} </template>
      </el-table-column>
      <el-table-column prop="description" label="项目描述" min-width="80">
      <template slot-scope="scope"> {{ scope.row.fields.description }} </template>
      </el-table-column>
      <el-table-column prop="status" label="项目状态" min-width="80">
      <template slot-scope="scope" >{{ scope.row.fields.status == 1 ? '有效':'无效' }}</template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="mini"
            circle
            plain
            @click.stop="handleUpdate(scope.row.pk)"
          />
          <el-button
            type="danger"
            icon="el-icon-delete"
            size="mini"
            circle
            plain
            @click.stop="handleDelete(scope.row.pk)"
          />
        </template>
      </el-table-column>
    </el-table>
    <div class="sc-pagination-container">
     <ul >
      <el-pagination
        background
        layout="total,prev, pager, next"
        v-show="pagination.total>0"
        :total="pagination.total"
        :page-size="pagination.limit"
        @current-change="handleCurrentChange">
      </el-pagination>
     </ul>
 </div>

    <!-- 表单弹窗 -->
    <el-dialog :title="dialog.title" :visible.sync="dialog.visible" width="600px">
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">

        <el-row>
          <el-col :span="18">
            <el-form-item label="项目名称" prop="prj_name">
              <el-input v-model="form.prj_name" placeholder="请输入项目名称"/>
            </el-form-item>
          </el-col>
          <el-col :span="18">
            <el-form-item label="项目版本" prop="version">
              <el-input v-model="form.version" placeholder="请输入项目版本"/>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="18">
            <el-form-item label="项目状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio  label="true">有效</el-radio>
                <el-radio  label="false">无效</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="项目描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="项目描述"/>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
        <el-button @click="dialog.visible=false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import {getproject,detail,update,add,del} from '@/api/project'
export default {
  // name: 'test1',
  data () {
    return {
      input: '',
      projectList: [],
      loading: false,
      meg:'',
      queryParams: {
          project_name: undefined
        },
      dialog: {
          title: undefined,
          visible: false,
          type: undefined  // type 操作类型：1-新增 2-修改
        },
      pagination: {
          page: 1,
          limit: 5,
          total: 0
        },
      form: {
          // authorizedGrantTypes: [],
          prj_id:undefined,
          prj_name: undefined,
          version: undefined,
          status: "true",
          description: undefined,
          // authorities: undefined,
          // additionalInformation: undefined,
          // autoapprove: 'false'
        },
      rules: {
          prj_name: [
            {required: true, message: '项目名称不能为空', trigger: 'blur'}
          ],
          version: [
            {required: true, message: '项目版本不能为空', trigger: 'blur'}
          ],
          status: [
            {required: true, message: '项目状态不能为空', trigger: 'blur'}
          ],
          description: [
            {required: false, message: '请输入接口描述', trigger: 'blur'}
          ]
        }
    }
  },
  mounted: function () {
    this.showProject()
  },
  methods: {
    showProject () {
        this.queryParams.page=this.pagination.page
        this.queryParams.limit=this.pagination.limit
        getproject(this.queryParams).then((response) => {
          this.projectList = response.data.data
          this.pagination.total=response.data.totalCount
        })
    },
    handleAdd() {
        this.resetForm()
        this.dialog = {
          title: '新增项目',
          visible: true,
          type: 'add'
        }
      },
    handleUpdate(row) {
        // this.resetForm()
        this.dialog = {
          title: '修改项目',
          visible: true,
          type: 'edit'
        }
        const id = row
        detail(id).then(response => {
          
          this.form = response.data[0].fields
          this.form.prj_id=response.data[0].pk
          if(response.data[0].fields.status==1){
              this.form.status="true"
          }else{
              this.form.status="false"
          }
          console.log(this.form)
          // if (data.authorizedGrantTypes) {
          //   this.form.authorizedGrantTypes = data.authorizedGrantTypes.split(',')
          // }
        })
      },
     closeDialog() {
        this.dialog = {
          title: undefined,
          visible: false,
          type: undefined
        }
      },
    resetForm() {
        this.form = {
          prj_id:undefined,
          prj_name: undefined,
          version: undefined,
          status: "true",
          description: undefined,
        }
        if (this.$refs['form']) {
          this.$refs['form'].resetFields()
        }
      },
    handleSubmit: function () {
        this.$refs['form'].validate(valid => {
          if (valid) {
            // this.form.authorizedGrantTypes = this.form.authorizedGrantTypes.join(',')
            if (this.dialog.type == 'edit') {
              update(this.form.prj_id, this.form).then(() => {
                this.$message.success('修改成功')
                this.closeDialog()
                this.showProject()
              })
            } else {
              add(this.form).then(() => {
                this.$message.success('新增成功')
                this.closeDialog()
                this.showProject()
              })
            }
          }
        })
      },
    handleDelete(prj_id) {
        this.$confirm('确认删除该项目?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          del(prj_id).then(() => {
            this.$message.success('删除成功')
            this.showProject()
          })
        }).catch(() =>
          this.$message.info('已取消删除')
        )
      },
    handleReset() {
        this.pagination = {
          page: 1,
          limit: 5,
          total: 0
        }
        this.queryParams = {
          project_name: undefined
        }
        this.showProject()
      },
      handleCurrentChange(val) {
        this.pagination.page=val
        this.queryParams.page=this.pagination.page
        this.queryParams.limit=this.pagination.limit
        getproject(this.queryParams).then((response) => {
          this.projectList = response.data.data
          this.pagination.total=response.data.totalCount
        })
      }
  },
  components:{
    
  }

}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }


  ul {
  list-style-type: none;
  padding: 0;
}


li {
  display: inline-block;
  margin: 0 5px;
}


a {
  color: #42b983;
}
</style>



