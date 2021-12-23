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
      <el-form-item prop="env_name">
        <el-input
          v-model="queryParams.env_name"
          placeholder="接口名称"
          clearable
          style="width: 220px"
          @keyup.enter.native="showEnv"
        />
        <el-select v-model="queryParams.project" placeholder="所属项目" style="width: 140px" >
           <el-option v-for="item in options" :key="item.prj_id" :label="item.prj_name" :value="item.prj_id"/>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="showEnv">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 列表数据 -->
    <el-table v-loading="loading"
              :data="envList"
              border             
    >
      <el-table-column prop="env_name" label="环境名称" min-width="80">
      <template slot-scope="scope"> {{ scope.row.fields.env_name }} </template>
      </el-table-column>
      <el-table-column prop="url" label="URL" min-width="100">
      <template slot-scope="scope"> {{ scope.row.fields.url }} </template>
      </el-table-column>
      <el-table-column prop="description" label="环境描述" min-width="80">
      <template slot-scope="scope"> {{ scope.row.fields.description }} </template>
      </el-table-column>
      <el-table-column prop="project" label="所属项目" min-width="80">
      <template slot-scope="scope"> 
        {{ get_map_prj(scope.row.fields.project) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="环境状态" min-width="80">
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
            <el-form-item label="环境名称" prop="env_name">
              <el-input v-model="form.env_name" placeholder="请输入环境名称"/>
            </el-form-item>
          </el-col>
          <el-col :span="18">
            <el-form-item label="URL" prop="url">
              <el-input v-model="form.url" placeholder="请输入url地址"/>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
        <el-col :span="12">
            <el-form-item label="所属项目" prop="project">
              <el-select v-model="form.project" placeholder="请选择">
                <el-option
                  v-for="item in options"
                  :key="item.prj_id"
                  :label="item.prj_name"
                  :value="item.prj_id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          </el-row>
        <el-row>
          <el-col :span="18">
            <el-form-item label="环境状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio  label="true">有效</el-radio>
                <el-radio  label="false">无效</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="环境描述" prop="description">
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
import {getenv,detail,del,update,add} from '@/api/environment'
import {getprj} from '@/api/interface';
export default {
  // name: 'test1',  组件
  data () {
    return {
      input: '',
      envList: [],
      loading: false,
      options: [],
      meg:'',
      queryParams: {
          env_name: undefined,
          project:undefined
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
          env_id:undefined,
          env_name: undefined,
          url: undefined,
          project:undefined,
          status: "true",
          description: undefined,
        },
      rules: {
          env_name: [
            {required: true, message: '环境名称不能为空', trigger: 'blur'}
          ],
          url: [
            {required: true, message: 'URL不能为空', trigger: 'blur'}
          ],
          project:[
            {required:true,message:'请选择所属项目',trigger:'blur'}
          ],
          status: [
            {required: true, message: '环境状态不能为空', trigger: 'blur'}
          ],
          description: [
            {required: false, message: '请输入接口描述', trigger: 'blur'}
          ]
        }
    }
  },
  mounted: function () {
    this.getprojectparm();
    this.showEnv()
  },
  methods: {
    showEnv () {
        this.queryParams.page=this.pagination.page
        this.queryParams.limit=this.pagination.limit
        getenv(this.queryParams).then((response) => {
          this.envList = response.data.data
          this.pagination.total=response.data.totalCount
        })
    },
    handleAdd() {
        this.resetForm()
        this.dialog = {
          title: '新增接口',
          visible: true,
          type: 'add'
        }
      },
    handleUpdate(row) {
        this.dialog = {
          title: '修改接口',
          visible: true,
          type: 'edit'
        }
        const id = row
        detail(id).then(response => {
          
          this.form = response.data[0].fields
          this.form.env_id=response.data[0].pk
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
          env_id:undefined,
          env_name: undefined,
          url: undefined,
          project:undefined,
          status: "true",
          description: undefined,
        }
        if (this.$refs['form']) {
          this.$refs['form'].resetFields()
        }
      },
    getprojectparm(){
        getprj().then((response)=>{
          this.options=response.data
        })
    },
    get_map_prj(project){
        let lable=""
        this.options.forEach(item=>{
          if(item.prj_id===project){
              lable=item.prj_name
          }
        })
        return lable
    },
    handleSubmit: function () {
        this.$refs['form'].validate(valid => {
          if (valid) {
            // this.form.authorizedGrantTypes = this.form.authorizedGrantTypes.join(',')
            if (this.dialog.type == 'edit') {
              update(this.form.env_id, this.form).then(() => {
                this.$message.success('修改成功')
                this.closeDialog()
                this.showEnv()
              })
            } else {
              add(this.form).then(() => {
                this.$message.success('新增成功')
                this.closeDialog()
                this.showEnv()
              })
            }
          }
        })
      },
    handleDelete(env_id) {
        this.$confirm('确认删除该项目?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          del(env_id).then(() => {
            this.$message.success('删除成功')
            this.showEnv()
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
          env_name: undefined,
          project:undefined
        }
        this.showEnv()
      },
      handleCurrentChange(val) {
        this.pagination.page=val
        this.queryParams.page=this.pagination.page
        this.queryParams.limit=this.pagination.limit
        getenv(this.queryParams).then((response) => {
          this.envList = response.data.data
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
  /* display: inline-block; */
  margin: 0 5px;
}


a {
  color: #42b983;
}
</style>



